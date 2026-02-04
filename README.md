# Supplementary code - Divergence of detachment forces in the finite-Voronoi model

[![arXiv:2503.03126](https://img.shields.io/badge/arXiv-26xx.xxxxx-grey.svg?colorB=a42c25&logo=arxiv)](https://doi.org/10.48550/arXiv.26xx.xxxxx)

This is the code required to reproduce the results in the paper:

- ***Divergence of detachment forces in the finite-Voronoi model***, Wei Wang (汪巍) and Brian A. Camley, **Soft Matter (2026)**.

Preprint version available on **arXiv**: [arXiv:26xx.xxxxx](https://doi.org/10.48550/arXiv.26xx.xxxxx).


## Requirements

The code was run with **Python 3.11.11** and the following packages:

* `numpy` == 2.1.3
* `matplotlib` == 3.10.0
* `scipy` == 1.5.3
* `pyafv` == 0.4.3 (core package; see our [GitHub repository](https://github.com/wwang721/pyafv))
* `tqdm` == 4.67.1
* `mpi4py` == 4.0.3
* `lifelines` == 0.30.0

You can install all dependencies by running `pip install -r requirements.txt`.

> [!TIP]
> On some HPC clusters, global Python path can contaminate the runtime environment. You may need to clear it explicitly by prefixing the `pip` command with `PYTHONPATH=""` or by running `unset PYTHONPATH`.


## Usage

### Figure 1

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pyafv/assets/blob/main/jupyter/custom_plot.ipynb)

Figure 1 is the plotting example shown in the `pyafv` documentation; click the badge above to run the notebook directly on **Google Colab**.


### Figure 2

Run [time_step/main.py](/time_step/main.py) (modify the time step $\Delta t$ in line 60) to generate simulation snapshots saved in the [time_step/frames](/time_step/frames/) directory.

> [WIP] Panels (b) and (c)...


### Figure 4

To compare the theory with the simulation results shown in panel (a), run [truncation/comparison.py](/truncation/comparison.py). To compute the detachment forces in the finite-Voronoi model for a given value of $\delta$ ($=0.45$), run [truncation/detachment_forces.py](/truncation/detachment_forces.py).


### Figure 5

To generate the $P_0$—Λ phase digram for the steady-state $\ell_0$, run [truncation/plot_l0.py](/truncation/plot_l0.py).

> [!Note]
> You may see `RuntimeWarning` reporting "overflow encountered". These are benign: during the optimization process, some random trial points may overflow, but this does not affect the final minimized results.


### Figure 6

> [WIP] Note: remember to include plotting code for the deformable-polygon (DP) model...


### Other figures

The remaining figures are either purely theoretical or minor variants/extensions of those described above and can be generated following analogous procedures.


## License

This project is licensed under the [MIT License](/LICENSE), which permits use, modification, and distribution of the code with minimal restrictions.
