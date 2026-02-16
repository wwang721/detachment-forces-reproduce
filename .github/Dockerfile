# syntax=docker/dockerfile:1

FROM wwang721/pyafv:0.4.6

# 1. Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    openssh-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Download and Compile OpenMPI
ENV OMPI_VERSION=3.1.6
ENV OMPI_URL="https://download.open-mpi.org/release/open-mpi/v3.1/openmpi-$OMPI_VERSION.tar.gz"

WORKDIR /tmp
# Added -Wno-int-conversion, -Wno-implicit-function-declaration, and -Wno-incompatible-pointer-types to CFLAGS
RUN wget -O openmpi.tar.gz $OMPI_URL && \
    tar -xzf openmpi.tar.gz && \
    cd openmpi-$OMPI_VERSION && \
    ./configure --prefix=/usr/local CFLAGS="-fcommon -Wno-int-conversion -Wno-implicit-function-declaration -Wno-incompatible-pointer-types" CXXFLAGS="-fcommon" && \
    make -j4 && \
    make install && \
    ldconfig && \
    cd .. && rm -rf openmpi-$OMPI_VERSION openmpi.tar.gz

# 3. Install mpi4py from source
RUN env MPICC=/usr/local/bin/mpicc pip install --no-cache-dir --no-binary=mpi4py mpi4py --break-system-packages

# 4. Create a non-root user
RUN useradd -m -s /bin/bash hpcuser
USER hpcuser
WORKDIR /home/hpcuser

# 5. Set paths
# Fixed the UndefinedVar warning by providing a default empty fallback for the variable
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH:-}"
ENV PATH="/usr/local/bin:$PATH"

# Default command
CMD ["python"]
