#!/bin/bash
#SBATCH --job-name=openmpbuild
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=00:05:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./build/bin/openmpbuild_out.%j.out
#SBATCH --error=./build/bin/openmpbuild_err.%j.out

### ------------------------------------------------------------------------ ###
### ------- You MUST edit these lines to set your default compiler(s) ------ ###
### --------- and optionally your environment, path to source and the -------- ###
### ----------------------- desired build directory  ----------------------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all
module load intel-oneapi-compilers/2023.2.1-gcc-11.2.0
spack load openmpi@4.1.5%oneapi
spack load cmake@3.23.1%oneapi
gxx="/sw/spack-levante/openmpi-4.1.6-ux3zoj/bin/mpic++"
gcc="/sw/spack-levante/openmpi-4.1.6-ux3zoj/bin/mpicc"

path2src=$1    # required
path2build=$2   # required
### ------------------------------------------------------------------------ ###

### ---------------------------------------------------- ###
### ------- You can optionally edit the following ------ ###
### -------- lines to customise your compiler(s) ------- ###
###  ------------ and build configuration  ------------- ###
### ---------------------------------------------------- ###

### --------- choose C/C++ compiler and flags ---------- ###
CC=${gcc}               # C
CXX=${gxx}              # C++

# CMAKE_CXX_FLAGS="-Werror -Wall -Wextra -pedantic -Wno-unused-parameter -g -gdwarf-4 -O0" # correctness and debugging
CMAKE_CXX_FLAGS="-Werror -Wall -Wextra -pedantic -Wno-unused-parameter -O3 -fma"           # performance
### ---------------------------------------------------- ###

### ------------ choose Kokkos configuration ----------- ###
# flags for serial kokkos
kokkosflags="-DKokkos_ARCH_ZEN3=ON -DKokkos_ENABLE_SERIAL=ON"

# flags for host parallelism (e.g. using OpenMP)
kokkoshost="-DKokkos_ENABLE_OPENMP=ON"

# flags for device parallelism (e.g. on gpus)
kokkosdevice=""
### ---------------------------------------------------- ###

### ------------------ choose YAC build ---------------- ###
yacflags="-DENABLE_YAC_COUPLING=OFF"
### ---------------------------------------------------- ###

### ---------------- build source with cmake ------------- ###
echo "CXX_COMPILER=${CXX} CC_COMPILER=${CC}"
echo "SRC_DIR: ${path2src}"
echo "BUILD_DIR: ${path2build}"
echo "KOKKOS_FLAGS: ${kokkosflags}"
echo "KOKKOS_DEVICE_PARALLELISM: ${kokkosdevice}"
echo "KOKKOS_HOST_PARALLELISM: ${kokkoshost}"
echo "CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}"

cmake -DCMAKE_CXX_COMPILER=${CXX} \
    -DCMAKE_C_COMPILER=${CC} \
    -DCMAKE_CXX_FLAGS="${CMAKE_CXX_FLAGS}" \
    -DCMAKE_MODULE_PATH=${yacmodule} \
    -S ${path2src} -B ${path2build} \
    ${kokkosflags} ${kokkosdevice} ${kokkoshost} \
    ${yacflags}
make -C ${path2build} -j 128

### ---------------------------------------------------- ###
