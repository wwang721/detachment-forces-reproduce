# Supplementary code - Divergence of detachment forces in the finite-Voronoi model

[![arXiv:2503.03126](https://img.shields.io/badge/arXiv-26xx.xxxxx-grey.svg?colorB=a42c25&logo=arxiv)](https://doi.org/10.48550/arXiv.26xx.xxxxx)

This is the code required to reproduce the results in the paper:

***Divergence of detachment forces in the finite-Voronoi model***, Wei Wang (汪巍) and Brian A. Camley, **Soft Matter (2026)**.

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




### Figure 4




### Figure 5




### Figure 6




### Other figures

The remaining figures are either purely theoretical or minor variants/extensions of those described above and can be generated following analogous procedures.


## License

This project is licensed under the [MIT License](/LICENSE), which permits use, modification, and distribution of the code with minimal restrictions.
