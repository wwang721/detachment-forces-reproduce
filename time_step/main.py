import numpy as np
import pyafv as afv
import matplotlib.pyplot as plt
from tqdm import tqdm


def custom_plot_2d(pts: np.ndarray, diag: dict, r: float, lw=1., markersize=1., ax=None):
    """
    Custom plot function
    """
    if ax is None:
        ax = plt.gca()

    point_edges_type = diag["edges_type"]
    point_vertices_f_idx = diag["regions"]
    vertices_all = diag["vertices"]

    # Draw cell centers
    ax.plot(pts[:, 0], pts[:, 1], 'o', color='C1',
            markersize=markersize, zorder=3)

    N = len(pts)

    # Draw each cell boundary
    for idx in range(N):
        edges_type = point_edges_type[idx]
        vertices_f_idx = point_vertices_f_idx[idx]

        x, y = pts[idx]
        if len(edges_type) < 2:
            angle = np.linspace(0, 2*np.pi, 100)
            ax.plot(x + r * np.cos(angle), y + r *
                    np.sin(angle), color="C4", lw=lw, zorder=1)
            # ax.fill(x + r * np.cos(angle), y + r * np.sin(angle), color="C3", alpha=0.2, zorder=0)
            continue

        for idx_f, edge_type in enumerate(edges_type):
            v1_idx = vertices_f_idx[idx_f]
            x1, y1 = vertices_all[v1_idx]
            idx2 = idx_f + 1 if idx_f < len(edges_type)-1 else 0
            v2_idx = vertices_f_idx[idx2]
            x2, y2 = vertices_all[v2_idx]

            if edge_type == 1:
                ax.plot([x1, x2], [y1, y2], color="C0", lw=lw, zorder=2)
                # ax.fill([x1, x2, x], [y1, y2, y], 'C3', alpha=0.2, zorder=0)
            else:
                angle1 = np.arctan2(y1-y, x1-x)
                angle2 = np.arctan2(y2-y, x2-x)
                dangle = np.linspace(0, (angle1 - angle2) % (2*np.pi), 100)

                ax.plot(x + r * np.cos(angle2+dangle), y + r *
                        np.sin(angle2+dangle), color="C4", lw=lw, zorder=1)
                # ax.fill(np.append(x + r * np.cos(angle2+dangle), x), np.append(y + r * np.sin(angle2+dangle), y), color="C3", alpha=0.2, lw=0, zorder=0)

    ax.set_aspect("equal")
    return ax


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
phys = afv.PhysicalParams(r=radius, A0=A0, P0=P0, lambda_tension=tension_difference, delta=0.0)
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
        custom_plot_2d(pts, diag, r=1)
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
