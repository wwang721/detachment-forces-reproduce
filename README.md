# Supplementary code & data - Divergence of detachment forces in the finite-Voronoi model

[![arXiv:2503.03126](https://img.shields.io/badge/arXiv-26xx.xxxxx-grey.svg?colorB=a42c25&logo=arxiv)](https://doi.org/10.48550/arXiv.26xx.xxxxx)
[![CI](https://github.com/wwang721/detachment-forces-reproduce/actions/workflows/ci.yml/badge.svg)](https://github.com/wwang721/detachment-forces-reproduce/actions/workflows/ci.yml)

These are the code and data required to reproduce the results in the paper:

- ***Divergence of detachment forces in the finite-Voronoi model***, Wei Wang (汪巍) and Brian A. Camley, **Soft Matter (2026)**.

Preprint version available on **arXiv**: [arXiv:26xx.xxxxx](https://doi.org/10.48550/arXiv.26xx.xxxxx).


## Requirements

The code was run with **Python 3.11.11** and the following packages:

| Package    | Version | Usage                                                                        |
| :--------- | :-----: | :--------------------------------------------------------------------------- |
| numpy      | 2.1.3   | Numerical computations                                                       |
| matplotlib | 3.10.0  | Plotting and visualization                                                   |
| scipy      | 1.15.3  | Miscellaneous scientific functions                                           |
| pyafv      | 0.4.5   | Core package; see our [GitHub repository](https://github.com/wwang721/pyafv) |
| tqdm       | 4.67.1  | Progress bars during calculations                                            |
| mpi4py     | 4.0.3   | Parallel processing using MPI                                                |
| lifelines  | 0.30.0  | Survival analysis                                                            |

You can install all dependencies by running `pip install -r requirements.txt`.

> [!TIP]
> On some HPC clusters, global Python path can contaminate the runtime environment. You may need to clear it explicitly by prefixing the `pip` command with `PYTHONPATH=""` or by running `unset PYTHONPATH`.


## Usage

### Figure 1

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pyafv/assets/blob/main/jupyter/custom_plot.ipynb)

Figure 1 is the plotting example given by the `pyafv` documentation; click the badge above to run the notebook directly on **Google Colab**.


### Figure 2

Run [time_step/main.py](/time_step/main.py) (modify the time step $\Delta t$ in line 60) to generate simulation snapshots saved in the [time_step/frames](/time_step/frames/) directory.

Submit the job to the HPC cluster using [time_step/run.slurm](/time_step/run.slurm) to run [time_step/scan_dt.py](/time_step/scan_dt.py) with two values of $\delta$ ($0$ and $0.45$). The simulation outputs are saved in [time_step/data](/time_step/data). Panels (b) and (c) are then produced by executing [time_step/analysis/KMF_survival.py](/time_step/analysis/KMF_survival.py) and [time_step/analysis/median.py](/time_step/analysis/median.py).


### Figure 4

To compare the theory with the simulation results shown in panel (a), run [truncation/comparison.py](/truncation/comparison.py). To compute the detachment forces in the finite-Voronoi model for a given value of $\delta$ ($=0.45$), run [truncation/detachment_forces.py](/truncation/detachment_forces.py).


### Figure 5

To generate the $P_0$—Λ phase digram for the steady-state $\ell_0$, run [truncation/plot_l0.py](/truncation/plot_l0.py).


### Figure 6

Run [calibration/main.py](/calibration/main.py) to execute the simulation and generate snapshots of a cell doublet subjected to external force dipoles in the deformable-polygon (DP) model.

To sweep the $P_0$—Λ parameter plane for detachment forces in DP model, submit [calibration/run.slurm](/calibration/run.slurm), which executes [calibration/dp_detach.py](/calibration/dp_detach.py). The results are saved to [calibration/detachment_forces_DP.npy](/calibration/detachment_forces_DP.npy). Then run [calibration/plot.py](/calibration/plot.py) to generate panel (b).

> [!NOTE]
> The `auto_calibrate` method used in [calibration/dp_detach.py](/calibration/dp_detach.py) also returns the steady-state cell radius $\ell_0$ and the target $\delta$ value that matches the detachment forces between the deformable-polygon (DP) and finite-Voronoi (FV) models; these quantities can also be saved and reused if needed.

The directory [calibration/fix_delta](/calibration/fix_delta/) contains the scripts for the fixed-delta calibration with $\delta=0.45$. The scripts [force_dist_P0_4.8.py](/calibration/fix_delta/force_dist_P0_4.8.py) and [force_dist_P0_6.py](/calibration/fix_delta/force_dist_P0_6.py) generate the constitutive relations for $P_0=4.8$ and $P_0=6$, respectively [panels (c) and (d)].
The scripts used to generate the two phase diagrams [panels (e) and (f)] are located in the directory [calibration/fix_delta/phase_diagrams](/calibration/fix_delta/phase_diagrams/). Two separate jobs should be submitted using [run.slurm](/calibration/fix_delta/phase_diagrams/run.slurm) to execute [scan_P0_Lambda.py](/calibration/fix_delta/phase_diagrams/scan_P0_Lambda.py) and [scan_P0_v0.py](/calibration/fix_delta/phase_diagrams/scan_P0_v0.py), respectively. After the simulations complete, the phase diagrams can be generated by running [plot_P0_Lambda.py](/calibration/fix_delta/phase_diagrams/plot_P0_Lambda.py) and [plot_P0_v0.py](/calibration/fix_delta/phase_diagrams/plot_P0_v0.py), which read the output data saved in [data](/calibration/fix_delta/phase_diagrams/data/).

The directory [calibration/match_fdetach](/calibration/match_fdetach/) contains scripts for the calibration in which the detachment forces are matched between the FV and DP models. The scripts [force_dist_P0_4.8.py](/calibration/match_fdetach/force_dist_P0_4.8.py) and [force_dist_P0_6.py](/calibration/match_fdetach/force_dist_P0_6.py) generate the constitutive relations for $P_0=4.8$ and $P_0=6$, respectively [panels (g) and (h)].
The scripts used to generate the last two phase diagrams [panels (i) and (j)] are located in [calibration/match_fdetach/phase_diagrams](/calibration/match_fdetach/phase_diagrams/) and are organized in the same way as those in [calibration/fix_delta/phase_diagrams](/calibration/fix_delta/phase_diagrams/).


### Other figures

The remaining figures are either purely theoretical or minor variants/extensions of those described above and can be generated following analogous procedures.


## License

This project is licensed under the [MIT License](/LICENSE), which permits use, modification, and distribution of the code with minimal restrictions.
