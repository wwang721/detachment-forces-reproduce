# syntax=docker/dockerfile:1

FROM wwang721/pyafv:0.4.6

# 1. Set environment variables for OpenMPI
ENV OMPI_VERSION=3.1.6
ENV OMPI_URL="https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-$OMPI_VERSION.tar.gz"

WORKDIR /tmp

# 2. Combined build and purge step (to keep image size small)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        openssh-client \
        git && \
    \
    # --- Download and Compile OpenMPI ---
    wget -O openmpi.tar.gz $OMPI_URL && \
    tar -xzf openmpi.tar.gz && \
    cd openmpi-$OMPI_VERSION && \
    # Added flags to handle GCC 12+ strictness with older OpenMPI code
    ./configure --prefix=/usr/local \
        CFLAGS="-fcommon -Wno-int-conversion -Wno-implicit-function-declaration -Wno-incompatible-pointer-types" \
        CXXFLAGS="-fcommon" && \
    make -j"$(nproc)" && \
    make install && \
    ldconfig && \
    cd .. && \
    \
    # --- Install mpi4py from source ---
    # We force build from source to link against the specific OpenMPI we just built
    env MPICC=/usr/local/bin/mpicc pip install --no-cache-dir --no-binary=mpi4py mpi4py==4.1.1 --break-system-packages && \
    \
    # --- CLEANUP: The Purge ---
    # Removing compilers and source code in the same layer they were created
    apt-get purge -y build-essential wget git && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* openmpi-$OMPI_VERSION openmpi.tar.gz

# 3. Create a non-root user (Standard for MPI security/HPC best practice)
RUN useradd -m -s /bin/bash hpcuser
USER hpcuser
WORKDIR /home/hpcuser

# 4. Set paths for the installed MPI libraries
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH:-}"
ENV PATH="/usr/local/bin:$PATH"

CMD ["python"]
