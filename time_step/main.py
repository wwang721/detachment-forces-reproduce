import numpy as np
import pyafv as afv
import matplotlib.pyplot as plt
from tqdm import tqdm


dt = 0.01
# dt = 0.005

# Set parameters
N_cell = 100  # number of cells in the system
radius = 1    # the radius of cell, i.e. l in the paper
phi = 0.5     # packing fraction
P0 = 4.8
A0 = np.pi
tension_difference = 0.1           # \Lambda in the paper
box_size = np.sqrt(N_cell*np.pi/phi)


# Initial the cell center positions in the center of the box
pts = ((np.random.rand(N_cell, 2) - 0.5) * 0.3 + 0.5) * box_size
phys = afv.PhysicalParams(r=radius, A0=A0, P0=P0, Lambda=tension_difference, delta=0.0)
sim = afv.FiniteVoronoiSimulator(pts, phys)

# Relax to equilibrium first
T_init = 20.0
init_steps = int(T_init / dt)

for _ in tqdm(range(init_steps), desc="Relaxation"):
    diag = sim.build()
    pts += dt * diag['forces']
    sim.update_positions(pts)


# Active dynamics
T = 100.0
steps = int(T / dt)

Dr = 1.33
v0 = 1.5
theta = 2. * np.pi * np.random.rand(N_cell)

t = 0.0
for _ in tqdm(range(steps), desc="Active dynamics"):
    diag = sim.build()
    forces = diag["forces"]

    # Save frames
    if round(t, 5).is_integer():
        fig, ax = plt.subplots(figsize=(3, 3))
        afv.visualize_2d(pts, diag, r=radius, ax=ax, cell_colors=None,
                         show_points=True, point_size=1, point_colors='C1',
                         arc_colors='C4', auto_adjust_bounds=False)

        ax.tick_params(axis='both', length=0, labelbottom=False, labelleft=False)
        ax.set_title(f't={t:.0f}', fontsize=10)

        ax.set_xlim(0, box_size)
        ax.set_ylim(0, box_size)
        plt.savefig(f'frames/{t:.0f}.png', dpi=100, bbox_inches='tight')
        plt.close(fig)

    active_velocity = v0 * np.column_stack((np.cos(theta), np.sin(theta)))
    pts += (forces + active_velocity) * dt
    theta += np.sqrt(2 * Dr * dt) * np.random.randn(N_cell)  # Gaussian white noise

    sim.update_positions(pts)
    t += dt
