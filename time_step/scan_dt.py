import numpy as np
import argparse
from tqdm import tqdm
from mpi4py import MPI

from pyafv import PhysicalParams, FiniteVoronoiSimulator, select_daughter_cluster


parser = argparse.ArgumentParser()
parser.add_argument("--delta", type=float, required=True)
args = parser.parse_args()
delta = args.delta

# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if delta == 0.0:
    dts = [0.1, 0.05, 0.02, 0.01, 0.009, 0.008, 0.007, 0.006, 0.005]
else:
    dts = [0.1, 0.05, 0.02, 0.01, 0.005, 0.002, 0.001]

counter = 0
for dt in dts:
    if rank == 0:
        counter += 1
        print(f"\nRunning simulation for dt={dt}: {counter}/{len(dts)}")
    
    M = 480        # (# of local tasks * size) Total number of realizations

    # Parameters
    # time unit: 1 hour
    # length unit: 20 microns
    N_init = 100                    # number of cells
    radius = 1.0                    # radius of each cell [20 microns]
    phi = 0.5                       # packing fraction
    T = 1000.0                      # total simulation time
    steps = int(T/dt)               # number of time steps
    T_init = 20.0                   # initial relaxation time
    steps_init = int(T_init/dt)     # number of initial relaxation steps

    # box size, (for plots only)
    box_size = np.sqrt(N_init * np.pi * radius**2 / phi)   

    va = 1.5                # active velocity [30 microns/hr]
    ktheta = 0.             # Angle alignment strength [1/hr]
    mu = 1.0                # Mobility
    Dr = 1.33               # Noise strength [1/45min]


    # Physical parameters
    phys = PhysicalParams(
        r=radius,
        A0=np.pi, 
        P0=4.8,
        KA=1.0,
        KP=1.0,
        Lambda=0.1,
        delta=delta,
    )


    # Split realizations among processes
    M_local = M // size  # Number of realizations per process
    if rank < M % size:
        M_local += 1

    if rank == 0:
        pbar = tqdm(total=M_local, desc=f"Processing {counter}")

    # Store results
    rupture_times_local = []
    rupture_sizes_local = []

    # Process realizations
    for m in range(M_local):
        N = N_init
        pts = ((np.random.rand(N, 2) - 0.5) * 0.3)    # shape (N,2)
        pts *= box_size

        theta = 2. * np.pi * np.random.rand(N) - np.pi

        sim = FiniteVoronoiSimulator(pts, phys)

        rupture_time = 0.0  # Store rupture time
        rupture_size = 0    # Store rupture size

        # Initial relaxation
        for _ in range(steps_init):
            diag = sim.build()
            pts += mu * diag["forces"] * dt
            sim.update_positions(pts)

        # Simulation loop
        for t in range(steps):
            diag = sim.build()
            forces = diag["forces"]
            connect = diag["connections"]

            # randomly select a daughter cluster
            selected, N, connect = select_daughter_cluster(N, connect)
            if selected is not None:
                pts = pts[selected]
                theta = theta[selected]
                forces = forces[selected]
                
                rupture_time = t * dt
                rupture_size = N
                break

            vx = mu * forces[:, 0] + va * np.cos(theta)
            vy = mu * forces[:, 1] + va * np.sin(theta)
            theta0 = np.arctan2(vy, vx)
            
            # update position first to ensure Euler's method
            pts[:, 0] += vx * dt
            pts[:, 1] += vy * dt
            sim.update_positions(pts)

            dtheta = - ktheta * np.arctan2(np.sin(theta-theta0), np.cos(theta-theta0))
            # Gaussian white noise
            noise = np.sqrt(2 * Dr * dt) * np.random.randn(N)
            theta += dtheta * dt + noise

        if rank == 0:
            pbar.update(1)

        rupture_times_local.append(rupture_time)
        rupture_sizes_local.append(rupture_size)

    if rank == 0:
        pbar.close()

    # Gather results from all processes
    rupture_times_all = comm.gather(rupture_times_local, root=0)
    rupture_sizes_all = comm.gather(rupture_sizes_local, root=0)

    # Combine results on the root process
    if rank == 0:
        rupture_times_all = np.concatenate(rupture_times_all)
        rupture_sizes_all = np.concatenate(rupture_sizes_all)

        if delta == 0.0:
            file_name = 'data/dt%g.npz' % dt
        else:
            file_name = 'data/trunc_dt%g.npz' % dt

        np.savez(file_name, rupture_times=rupture_times_all, rupture_sizes=rupture_sizes_all)
        print('\nSaved data to %s' % file_name)

if rank == 0:
    print("Done.")
