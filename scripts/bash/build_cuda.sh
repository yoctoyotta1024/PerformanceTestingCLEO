#!/bin/bash
#SBATCH --job-name=cudaopenmpbuild
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=940M
#SBATCH --time=00:05:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./build/bin/cudaopenmpbuild_out.%j.out
#SBATCH --error=./build/bin/cudaopenmpbuild_err.%j.out

### ------------------------------------------------------------------------ ###
### ------- You MUST edit these lines to set your default compiler(s) ------ ###
### --------- and optionally your environment, path to source and the -------- ###
### ----------------------- desired build directory  ----------------------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all
# TODO(CB): get intel compiler to work for CUDA build
module load gcc/11.2.0-gcc-11.2.0 # bcn7mbu
spack load cuda@12.2.0%gcc@=11.2.0
spack load openmpi@4.1.2%gcc@11.2.0
spack load cmake@3.26.3%gcc@=11.2.0/fuvwuhz
gxx="/sw/spack-levante/openmpi-4.1.2-mnmady/bin/mpic++"
gcc="/sw/spack-levante/openmpi-4.1.2-mnmady/bin/mpicc"

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
CMAKE_CXX_FLAGS="-Werror -Wall -Wextra -pedantic -Wno-unused-parameter -O3 -mfma"                # performance
### ---------------------------------------------------- ###

### --------------- choose CUDA compiler --------------- ###
# set nvcc compiler used by Kokkos nvcc wrapper as CUDA_ROOT/bin/nvcc
# NOTE(!) this path should correspond to the loaded nvhpc/cuda module.
# you can get a clue for the correct path e.g. via 'spack find -p cuda@11.8'
CUDA_ROOT="/sw/spack-levante/cuda-12.2.0-2ttufp/"

# set default (C++) compiler used by kokkos nvcc wrapper
# (wrapper is found in bin directory of Kokkos after its
# installation e.g. build/_deps/kokkos-src/bin/nvcc wrapper)
NVCC_WRAPPER_DEFAULT_COMPILER=${gxx}
### ---------------------------------------------------- ###

### ------------ choose Kokkos configuration ----------- ###
# flags for serial kokkos
kokkosflags="-DKokkos_ARCH_ZEN3=ON -DKokkos_ARCH_AMPERE80=ON -DKokkos_ENABLE_SERIAL=ON"

# flags for host parallelism (e.g. using OpenMP)
kokkoshost="-DKokkos_ENABLE_OPENMP=ON"

# flags for device parallelism (e.g. on gpus)
kokkosdevice="-DKokkos_ENABLE_CUDA=ON -DKokkos_ENABLE_CUDA_LAMBDA=ON \
-DKokkos_ENABLE_CUDA_CONSTEXPR=ON -DKokkos_ENABLE_CUDA_RELOCATABLE_DEVICE_CODE=ON \
-DCUDA_ROOT=${CUDA_ROOT} -DNVCC_WRAPPER_DEFAULT_COMPILER=${NVCC_WRAPPER_DEFAULT_COMPILER}"
### ---------------------------------------------------- ###

### ------------------ choose YAC build ---------------- ###
yacflags="-DENABLE_YAC_COUPLING=OFF"
### ---------------------------------------------------- ###

### ---------------- build source with cmake ------------- ###
echo "CXX_COMPILER=${CXX} CC_COMPILER=${CC}"
echo "CUDA=${CUDA_ROOT}/bin/nvcc (via Kokkos nvcc wrapper)"
echo "NVCC_WRAPPER_DEFAULT_COMPILER=${NVCC_WRAPPER_DEFAULT_COMPILER}"
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
