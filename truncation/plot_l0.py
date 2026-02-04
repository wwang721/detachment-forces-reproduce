import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pyafv as afv


KA = 1.0
KP = 1.0
A0 = np.pi

P0s = np.linspace(4., 2*np.pi, 20)
Lambdas = np.linspace(0., 0.5, 20)

X, Y = np.meshgrid(P0s, Lambdas)

l0_values = np.zeros((len(Lambdas), len(P0s)))

for i, Lambda in enumerate(Lambdas):
    for j, P0 in enumerate(P0s):
        phys = afv.PhysicalParams(KA=KA, KP=KP, A0=A0, P0=P0, lambda_tension=Lambda)
        l, d = phys.get_steady_state()
        l0_values[i, j] = l  # record the minimized l0


# ---- Plot the phase diagram ----
fig, ax = plt.subplots(figsize=(2.6, 3))

min_l0 = np.min(l0_values)
max_l0 = np.max(l0_values)
cmap = plt.cm.bwr

# make 1 correspond to white color in the colormap
blue_part =np.linspace(0., 0.5, 256)
red_part = np.linspace(0.5, 0.9, int(256 * (max_l0 - 1.0) / (1.0 - min_l0)))[1:]
cmap_new = mcolors.LinearSegmentedColormap.from_list("truncated_bwr", cmap(np.concatenate((blue_part, red_part))))

background = ax.pcolormesh(X, Y, l0_values, shading='auto', vmax=max_l0, vmin=min_l0, cmap=cmap_new)
cbar = plt.colorbar(background, ax=ax, location='top', fraction=0.05, aspect=11, pad=0.03)

cbar.ax.text(1.12, 0.3, r'$\ell_0$', fontsize=13, transform=cbar.ax.transAxes)

cbar.outline.set_linewidth(0)
cbar.ax.tick_params(axis='both', which='major', direction='in', labelsize=11, pad=0)
cbar.ax.tick_params(axis='both', which='major', width=0.5, length=2)

# Move colorbar position
pos = cbar.ax.get_position()
dx = 0.03
cbar.ax.set_position([pos.x0 - dx, pos.y0, pos.width, pos.height])

ax.set_xlabel(r"$P_0$")
ax.set_ylabel(r"$\Lambda$")

# add minor ticks
ax.set_xticks([4.5, 5.5], minor=True)

ax.set_xlim(left=4, right=2*np.pi)
ax.set_ylim(bottom=0, top=0.5)

plt.savefig("optimal_l0.png", dpi=150, bbox_inches='tight')
