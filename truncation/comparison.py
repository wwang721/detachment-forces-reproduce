import numpy as np
import pyafv as afv
import matplotlib.pyplot as plt

# Initialize simulator with two particles
l = 1.0        # maximum cell radius
KA = 1.0
KP = 1.0
A0 = np.pi
P0 = 4.8
Lambda = 0.2

phys = afv.PhysicalParams(r=l, A0=A0, P0=P0, KA=KA, KP=KP, lambda_tension=Lambda, delta=0.0)
sim = afv.FiniteVoronoiSimulator(np.zeros((2,2)), phys)

ds = np.arange(1e-3, 2, 1e-3)  # distances between cell centers
forces = []
for d in ds:
    pts = np.array([[0, 0], [d, 0]])
    sim.update_positions(pts)
    diag = sim.build()
    force = diag['forces'][0,0]  # force on first cell, x-component
    forces.append(force)

# Now with truncation
sim.update_params(phys.replace(delta=0.45))
forces_trunc = []
for d in ds:
    pts = np.array([[0, 0], [d, 0]])
    sim.update_positions(pts)
    diag = sim.build()
    force = diag['forces'][0, 0]  # force on first cell, x-component
    forces_trunc.append(force)


#================================
# Plot
#================================

fig, ax = plt.subplots(figsize=(3, 3))

# Theoretical results
distances = np.linspace(1e-6, 2-(1e-6), 1000)
detachment_forces = []
for distance in distances:
    epsilon = l - (distance/2.)
    theta = 2 * np.pi - 2 * np.arctan2(np.sqrt(l**2 - (l - epsilon)**2), l - epsilon)
    A = (l - epsilon) * np.sqrt(l**2 - (l - epsilon)**2) + 0.5 * (l**2 * theta)
    P = 2 * np.sqrt(l**2 - (l - epsilon)**2) + l * theta
    f = 4. * np.sqrt((2-epsilon) * epsilon) * (A - A0 + KP * ((P - P0)/(2 - epsilon)) + (Lambda/2) * (1./((2-epsilon)*epsilon)))
    detachment_forces.append(f)

ax.plot(distances, detachment_forces, label=r'Analytical', lw=2, color='k', alpha=0.8, zorder=1)

distances = np.linspace(1.3, 2-(1e-6), 1000)
detachment_forces_asympt = []
for distance in distances:
    epsilon = l - (distance/2.)
    f2 = -2. * np.sqrt(2*epsilon) * (2 * A0 - 2 * np.pi + KP * (P0 - 2 * np.pi) - Lambda/(2*epsilon))
    detachment_forces_asympt.append(f2)

ax.plot(distances, detachment_forces_asympt, '--', lw=2, color='k', zorder=2)

#-----------------------------------------------------
# Simulation results

step = 30
data = np.column_stack((ds, forces))
ax.plot(data[:-25:step, 0], data[:-25:step, 1], 'o', color="C0", markerfacecolor='None', label='Original', zorder=0, clip_on=False)
ax.plot(data[-35, 0], data[-35, 1], 'o', color="C0", markerfacecolor='None', zorder=0, clip_on=False)
ax.plot(data[-25::5, 0], data[-25::5, 1], 'o', color="C0", markerfacecolor='None', zorder=0, clip_on=False)

data = np.column_stack((ds, forces_trunc))
ax.plot(data[::step, 0], data[::step, 1], '^', color="C3", markerfacecolor="None", label='Truncated', zorder=0, clip_on=False)


ax.axvline(x=2, color='C7', alpha=0.2, zorder=-1)
ax.axhline(y=0, color='C7', alpha=0.2, zorder=-1)
ax.set_ylim(-6, 6)
ax.set_xlim(0, 2.1)
ax.legend(frameon=False, loc='upper left', fontsize=11.5)
ax.set_xlabel(r'Distance $d$')
ax.set_ylabel(r'Force $f$')

#---------------------------------------------
# Add inset

from mpl_toolkits.axes_grid1.inset_locator import inset_axes
axins = inset_axes(ax, width="45%", height="35%", loc='lower left', bbox_to_anchor=(0.43, 0.08, 1, 1), bbox_transform=ax.transAxes)


# change font size for inset
axins.tick_params(axis='both', which='major', labelsize=11)
axins.plot(distances, detachment_forces_asympt, '--', lw=2, color='k', zorder=2)

xleft, xright = 1.8, 2
ylower, yupper = 2, 4
data = np.column_stack((ds, forces))
mask = data[:, 0] >= xleft
mask &= data[:, 1] <= yupper 
mask &= data[:, 1] >= ylower
data = data[mask]

step = 6
axins.plot(data[:-25:step, 0], data[:-25:step, 1], 'o',  color="C0", markerfacecolor='None', zorder=0, clip_on=False)
axins.plot(data[-25::3, 0], data[-25::3, 1], 'o', color="C0", markerfacecolor='None', zorder=0, clip_on=False)

data = np.column_stack((ds, forces_trunc))
mask = data[:, 0] >= xleft
mask &= data[:, 1] <= yupper
mask &= data[:, 1] >= ylower
data = data[mask]
axins.plot(data[::step, 0], data[::step, 1], '^', color="C3", markerfacecolor="None", zorder=0, clip_on=False)

axins.set_xlim(xleft, xright)
axins.set_ylim(ylower, yupper)
# add minor ticks
axins.set_xticks([1.85, 1.95], minor=True)
ax.set_xticks([0, 0.5, 1, 1.5, 2])
ax.set_xticklabels(['0', '0.5', '1.0', '1.5', '2.0'])

plt.savefig('comparison.png', dpi=150, bbox_inches='tight')
