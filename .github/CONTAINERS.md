# Containers

[![Docker](https://img.shields.io/docker/pulls/wwang721/pyafv.svg?logo=docker)](https://hub.docker.com/r/wwang721/pyafv)
[![Docker image build and push](https://github.com/wwang721/detachment-forces-reproduce/actions/workflows/docker.yml/badge.svg)](https://github.com/wwang721/detachment-forces-reproduce/actions/workflows/docker.yml)

## Docker image

The core package [**PyAFV**](https://github.com/wwang721/pyafv) provides a containerized installation via **Docker**:
```bash
docker pull wwang721/pyafv:latest
```
This command pulls the image from [**Docker Hub**](https://hub.docker.com/r/wwang721/pyafv). The same image is also available via the **GitHub Container Registry (GHCR)** under [**GitHub Packages**](https://github.com/wwang721/pyafv/pkgs/container/pyafv); use `ghcr.io/wwang721/pyafv` to pull from GHCR instead.
The default working directory inside the container is `/app`.
To run a Python script using `pyafv` from your current directory:
```bash
docker run --rm -v $(pwd):/app wwang721/pyafv python <script_name>.py
```
On Windows PowerShell, use `${PWD}` instead of `$(pwd)`.


## Singularity container on HPC

On many HPC clusters, Docker is not permitted, but **Singularity** (or Apptainer) is supported.
Load Singularity and pull the image from Docker Hub:
```bash
[userid@node ~]$ module load singularity
[userid@node ~]$ mkdir ~/singularity
[userid@node ~]$ cd ~/singularity/
[userid@node ~/singularity]$ singularity pull docker://wwang721/pyafv:latest
[userid@node ~/singularity]$ singularity shell pyafv_latest.sif
```
`pyafv_latest.sif` is the downloaded Singularity container image.
The last command opens an interactive shell inside the container.
To run a Python script without entering the shell:
```bash
singularity exec pyafv_latest.sif python <script_name>.py
```


### MPI-enabled container for HPC

A special Docker image including **pyafv** 0.4.8, **OpenMPI**, and the Python package `mpi4py` is also available on [Docker Hub](https://hub.docker.com/layers/wwang721/pyafv/rockfish-mpi).

This image has been tested on the **Rockfish** cluster (rockfish.jhu.edu) at Johns Hopkins University. For other systems, you may use the [Dockerfile](./Dockerfile) as a reference and adapt it to your environment.

> [!NOTE]
> The MPI ABI (Application Binary Interface) of the Docker image must be compatible with the MPI installation on your cluster (e.g., both use **OpenMPI** or both use **MPICH**).

The following instructions describe how to use this image as a Singularity container on Rockfish.
First, make sure you load `singularity` and `openmpi`, then
```bash
singularity pull docker://wwang721/pyafv:rockfish-mpi
```
Use the host (HPC) MPI installation to launch jobs on a single node:
```bash
mpiexec singularity exec pyafv_rockfish-mpi.sif python <script_name>.py
```

It is recommended to convert the `.sif` image into a sandbox directory for improved performance and flexibility:
```bash
[userid@node ~/singularity]$ singularity build --sandbox pyafv_sandbox_dir pyafv_rockfish-mpi.sif
```
Then use this in the job-submission script (e.g., SLURM) to launch jobs across multiple nodes:
```bash
module load singularity
module load openmpi

mpiexec \
    -mca btl_vader_single_copy_mechanism none \
    -mca btl_tcp_if_include ens0 \
    singularity exec ~/singularity/pyafv_sandbox_dir python your_script.py
```
The first `-mca` flag disables OpenMPI's shared-memory communication mechanism to avoid compatibility issues inside containers. In the second `-mca` flag, the network interface name `ens0` is specific to the Rockfish parallel partition. To determine the appropriate interface on your system, run
```bash
srun -N 1 --partition=YOUR_PARTITION ip -o -4 route show to default
```
to print your actual network interface.
