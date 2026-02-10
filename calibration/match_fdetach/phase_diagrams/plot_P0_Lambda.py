import matplotlib.pyplot as plt
import numpy as np
from lifelines import KaplanMeierFitter
from matplotlib.colors import LogNorm


P0s = np.linspace(4, 6, 11)
P0s = np.concatenate((P0s, [6.1, 6.2]))
Lambdas = np.linspace(0.0, 0.5, 11)  # Tension parameter values


dt = 0.01  # time step
medians = []
for P0 in P0s:
    ms = []
    for Lambda in Lambdas:
        
        data = np.load("./data/P0_%g_Lambda_%g.npz" % (P0, Lambda))
        
        rupture_times = data['rupture_times']
        rupture_sizes = data['rupture_sizes']

        # remove assays already rupture before starting time
        mask = (rupture_sizes > 0) & (rupture_times < dt)

        rupture_times = rupture_times[~mask]
        rupture_sizes = rupture_sizes[~mask]

        nExps = rupture_sizes.size  # number of assays
        rupture_times = rupture_times[rupture_sizes > 0]
        rupture_sizes = rupture_sizes[rupture_sizes > 0]
        N = len(rupture_times)  # number of assays that have ruptures

        if nExps == 0:
            N, nExps = 1, 1  # to avoid no data
            rupture_times = np.zeros(1)

        if N == 0:
            rupture_times = np.ones(1)

        T = np.ones(nExps) * rupture_times.max()
        T[:N] = rupture_times

        E = np.zeros(nExps)
        E[:N] = np.ones(N)

        kmf = KaplanMeierFitter()
        kmf.fit(T, event_observed=E, timeline=np.arange(0, 1000+dt, dt))

        median_ = kmf.median_survival_time_
        ms.append(median_)
    medians.append(ms)

medians = np.array(medians)


# Mask infinite values
masked_medians = np.ma.masked_invalid(medians)
mask_zero = masked_medians <= dt
masked_medians[mask_zero] = 0.
mask_inf = np.isinf(masked_medians)

# Create meshgrid
X, Y = np.meshgrid(P0s, Lambdas)

# Plot
fig, ax = plt.subplots(figsize=(3, 2.8))

iy, ix = np.where(mask_zero)
ax.scatter(X[ix, iy], Y[ix, iy], marker="x", color='C3', clip_on=False)

iy, ix = np.where(mask_inf)
ax.scatter(X[ix, iy], Y[ix, iy], marker="*", color='C4', clip_on=False)

ax.axvline(x=np.pi*2, color='gray', linestyle='--', label=r'$P_0=2\pi$', zorder=2)

background = ax.pcolormesh(X, Y, masked_medians.T, norm=LogNorm(), shading='auto', cmap='cool')
cbar = plt.colorbar(background, ax=ax)

cbar.ax.set_title(r'$t_{1/2}$', pad=8)

row_min_indices = np.argmin(medians, axis=1)

ax.set_ylabel(r'$\Lambda$')
ax.set_xlabel(r'$P_0$')

ax.set_title(r'$v_0=1.5$', pad=10)

ax.set_xticks([4.5, 5.5], minor=True)

ax.set_xlim(min(P0s), max(P0s))
ax.set_ylim(min(Lambdas), max(Lambdas))
plt.savefig('P0_Lambda.png', dpi=150, bbox_inches='tight')
