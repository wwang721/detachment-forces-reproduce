import numpy as np
from pyafv import FiniteVoronoiSimulator, PhysicalParams, target_delta, select_daughter_cluster
from tqdm import tqdm
from mpi4py import MPI


# MPI setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


P0s = np.linspace(4, 6, 11)
P0s = np.concatenate((P0s, [6.1, 6.2]))
Lambdas = np.linspace(0.0, 0.5, 11)  # Tension parameter values


counter = 0
for idx_Lambda, Lambda in enumerate(Lambdas):
    for idx_P0, P0_val in enumerate(P0s):
        if rank == 0:
            counter += 1
            print(f"\nRunning simulation for P0={P0_val:g}, Lambda={Lambda:g}: {counter}/{len(P0s)*len(Lambdas)}")

            # Physical parameters
            phys = PhysicalParams(A0=np.pi, P0=P0_val, KA=1.0, KP=1.0, Lambda=Lambda)
            phys = phys.with_optimal_radius()

            detachment_force = np.load('../../detachment_forces_DP.npy')[idx_P0, idx_Lambda]
            delta = target_delta(phys, detachment_force) if detachment_force > 0.0 else 0.0
            phys = phys.replace(delta=delta)
        else:
            phys = None

        phys = comm.bcast(phys, root=0)  # Broadcast phys to all processes

        if phys is None:
            raise ValueError("phys is None")


        M = 480        # (# of local tasks * size) Total number of realizations

        # Parameters
        # time unit: 1 hour
        # length unit: 20 microns
        N_init = 100                    # number of cells
        radius = phys.r                 # radius of each cell [20 microns]
        phi = 0.5                       # packing fraction
        dt = 0.002 if Lambda <= 0.2 else 0.006      # time step
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
            np.savez('data/P0_%g_Lambda_%g.npz' % (P0_val, Lambda), rupture_times=rupture_times_all, rupture_sizes=rupture_sizes_all)
            print('\nSaved data to data/P0_%g_Lambda_%g.npz' % (P0_val, Lambda))

if rank == 0:
    print("Done.")
