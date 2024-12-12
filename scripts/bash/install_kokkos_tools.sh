#!/bin/bash
#SBATCH --job-name=install_kokkos_tools
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=940M
#SBATCH --time=00:5:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./build/bin/install_kokkos_tools_out.%j.out
#SBATCH --error=./build/bin/install_kokkos_tools_err.%j.out

### ------------------------------------------------------- ###
### running script sucessfully installs kokkos tools for
### gcc 11.2.0 compiler on Levante assuming you have already performed
### STEP 1) ```git clone git@github.com:kokkos/kokkos-tools.git```
### in current working directory
### ------------------------------------------------------- ###
module purge
spack unload --all

root4tools=$1 # absolute path for kokkos-tools installation

cmake=cmake@3.23.1%gcc
gcc=gcc/11.2.0-gcc-11.2.0
CXX="/sw/spack-levante/gcc-11.2.0-bcn7mb/bin/g++" # must match gcc

if [ "${root4tools}" == "" ]
then
  echo "Bad input, please specify absolute path for where you want to install kokkos-tools"
else
  if [ ! -d "./kokkos-tools" ]; then
    echo "ERROR: kokkos-tools source directory not found. Please clone it into current working directory" >&2
    exit 1
  fi

  # STEP 2) build, make and install kokkos-tools
  module load ${gcc}
  spack load ${cmake}

  mkdir ${root4tools}
  cd ./kokkos-tools && mkdir ./myBuild
  cmake -DCMAKE_CXX_COMPILER=${CXX} -S ./ -B ./myBuild -DCMAKE_INSTALL_PREFIX=${root4tools}
  cd ./myBuild && make && make install
  echo "SUCCESS: kokkos-tools installed in ${root4tools}/"
fi


### STEP 3) profile executable
# example for for tools installed in /work/bm1183/m300950/kokkos_tools_lib/:
# A) see tool libraries installed in /work/bm1183/m300950/kokkos_tools_lib/lib64/
# B) export required tool library, e.g.
#     e.g. export KOKKOS_TOOLS_LIBS=/work/bm1183/m300950/kokkos_tools_lib/lib64/libkp_kernel_timer.so
#      or  export KOKKOS_TOOLS_LIBS=/work/bm1183/m300950/kokkos_tools_lib/lib64/libkp_space_time_stack.so
# C) run executable ./[exec].exe (kokkos initialise loads dynamic library pointers)
# D) read *.dat output
#     e.g. with kp reader
#          export LD_LIBRARY_PATH=/work/bm1183/m300950/kokkos_tools_lib/lib64/:$LD_LIBRARY_PATH
#          /work/bm1183/m300950/kokkos_tools_lib/bin/kp_reader *.dat > ./bin/kp_kernel_timer.txt
#    or pipe kp_space_time_stack output durign runtime: ./[exec].exe > runtime_output.txt
