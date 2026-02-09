import numpy as np
import matplotlib.pyplot as plt
from pyafv import PhysicalParams, FiniteVoronoiSimulator
from pyafv.calibrate import DeformablePolygonSimulator, polygon_centroid


P0 = 6.0
Lambda = 0.2

phys = PhysicalParams(P0=P0, Lambda=Lambda)
phys = phys.with_optimal_radius(delta=0.45)

l = phys.r
KP = phys.KP
A0 = phys.A0

fig, ax = plt.subplots(figsize=(2.8, 2.8))
step = 30

#====================================================
# Analytical results

distances = np.linspace(1e-6, 2*l-(1e-6), 1000)
detachment_forces = []

centroid_distances = []
for distance in distances:
    epsilon = l - (distance/2.)

    theta = 2 * np.pi - 2 * np.arctan2(np.sqrt(l**2 - (l - epsilon)**2), l - epsilon)
    A = (l - epsilon) * np.sqrt(l**2 - (l - epsilon)**2) + 0.5 * (l**2 * theta)
    P = 2 * np.sqrt(l**2 - (l - epsilon)**2) + l * theta

    f = 4. * np.sqrt((2*l-epsilon) * epsilon) * (A - A0 + KP * ((P - P0)/(2 * l - epsilon)) + (Lambda/2) * (l/((2*l-epsilon)*epsilon)))
    detachment_forces.append(f)

    phi = np.arctan2(np.sqrt(l**2 - (l - epsilon)**2), l - epsilon)
    Acap = l**2 * (phi - np.sin(phi) * np.cos(phi))
    xcap = 4.*l * np.sin(phi)**3/(3.*(2*phi - np.sin(2*phi)))
    Delta = Acap * xcap / (np.pi * l**2 - Acap)
    centroid_distances.append(distance + 2 * Delta)

ax.plot(centroid_distances, detachment_forces, "--", label=r'Analytical', lw=2, color="C0", zorder=1)

ax.axvline(x=2*l, color='C7', alpha=0.2, zorder=-1)
ax.axhline(y=0, color='C7', alpha=0.2, zorder=-1)


#====================================================
# Finite Voronoi results

distances = np.arange(0.001, 2*l, 0.001)
pts = np.array([[0, 0], [1, 0]], dtype=np.float64)

sim = FiniteVoronoiSimulator(pts, phys)

detachment_forces = []
for distance in distances:
    pts[1, 0] = distance
    sim.update_positions(pts)
    diag = sim.build()
    force = diag['forces'][0, 0]  # force on first cell, x-component
    detachment_forces.append(force)

data = np.column_stack((distances, detachment_forces))

epsilon = l - (distances/2.)
phi = np.arctan2(np.sqrt(l**2 - (l - epsilon)**2), l - epsilon)
Acap = l**2 * (phi - np.sin(phi) * np.cos(phi))
xcap = 4.*l * np.sin(phi)**3/(3.*(2*phi - np.sin(2*phi)))
Delta = Acap * xcap / (np.pi * l**2 - Acap)
centroid_distances = distances + 2 * Delta

mask = (data[:,1] > -3.5)
ax.plot(centroid_distances[mask][::step], data[mask,1][::step], 's', color="C4", markerfacecolor="None", label='FV', zorder=0, clip_on=False)


#====================================================
# Deformable polygon results

sim = DeformablePolygonSimulator(phys)
ext_forces = np.linspace(0, -3, 7)

centroid_distances = []
contact_lengths = []
for ext_force in ext_forces:

    if ext_force < 0:
        sim.simulate(ext_force, dt=0.001, nsteps=100_000)
        print(f"F_ext={ext_force} detached: {sim.detached}")

    C1 = polygon_centroid(sim.pts1)
    C2 = polygon_centroid(sim.pts2)
    centroid_distances.append(np.linalg.norm(C2 - C1))
    contact_lengths.append(sim.contact_length)

ax.plot(centroid_distances, ext_forces, '-o', color="C3", zorder=1)

ax2 = ax.twinx()
ax2.plot(centroid_distances, contact_lengths, '-x', color="C2", zorder=0)

f2save = ext_forces[-1:0:-1]
d2save = centroid_distances[-1:0:-1]
Pc2save = contact_lengths[-1:0:-1]

#---------------------------------------
sim = DeformablePolygonSimulator(phys)
ext_forces = np.linspace(0, 3, 7)

centroid_distances = []
contact_lengths = []
for ext_force in ext_forces:

    if ext_force > 0:
        sim.simulate(ext_force, dt=0.001, nsteps=100_000)
        print(f"F_ext={ext_force} detached: {sim.detached}")

    C1 = polygon_centroid(sim.pts1)
    C2 = polygon_centroid(sim.pts2)
    centroid_distances.append(np.linalg.norm(C2 - C1))
    contact_lengths.append(sim.contact_length)

f2save = np.concatenate((f2save, ext_forces))
d2save = np.concatenate((d2save, centroid_distances))
Pc2save = np.concatenate((Pc2save, contact_lengths))

np.save("force_dist_P0_6.npy", np.column_stack((d2save, f2save, Pc2save)))

ax.plot(centroid_distances, ext_forces, '-o', color="C3", label="DP", clip_on=False, zorder=2)
ax2.plot(centroid_distances, contact_lengths, '-x', color="C2", clip_on=False, zorder=0)


ax2.set_ylim(0, 3.5)
# Color the right axis green
ax2.tick_params(axis='y', colors='C2')
ax2.spines['right'].set_color('C2')
ax2.set_ylabel(r'Contact length $P^{(c)}$', color="C2", rotation=270, labelpad=25)


ax.set_xlabel(r'Centroid distance')
ax.set_ylabel(r'Force $f$')

ax.set_title(r'$P_0=6$')

ax.set_ylim(-3.5, 5)
ax.set_xlim(1.0, 2.615)
ax.legend(frameon=False, loc='upper left')

plt.savefig("force_dist_P0_6.png", dpi=150, bbox_inches='tight')
