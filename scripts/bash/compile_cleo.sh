#!/bin/bash
#SBATCH --job-name=compileexec
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --mem=30G
#SBATCH --time=00:30:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./compileexec_out.%j.out
#SBATCH --error=./compileexec_err.%j.out

### ------------------------------------------------------------------------ ###
### ----------------- PLEASE NOTE: this script assumes you ----------------- ###
### --------------- have already built CLEO in "path2build" ---------------- ###
### -----------------------  directory using cmake  ------------------------ ###
### ------------------------------------------------------------------------ ###

buildtype=$1      # get from command line argument
path2build=$2     # get from command line argument
executables="$3"  # get from command line argument

spack load cmake@3.23.1%gcc
module load gcc/11.2.0-gcc-11.2.0
source activate /work/bm1183/m300950/mambaenvs/perftests

if [ "${buildtype}" != "serial" ] && [ "${buildtype}" != "openmp" ] && [ "${buildtype}" != "cuda" ];
then
  echo "please specify the build type as 'serial', 'openmp' or 'cuda'"
else
  # load nvhpc compilers if compiling cuda build
  if [[ "${buildtype}" == "cuda" ]]
  then
    module load nvhpc/23.9-gcc-11.2.0
  fi
  ### ---------------------------------------------------- ###

  if [[ "${buildtype}" == "" ||
        "${path2build}" == "" ||
        "${executables}" == "" ]]
  then
    echo "Bad inputs, please check your buildtype, path2build and executables"
  else
    ### ---------------- compile executables --------------- ###
    echo "path to build directory: ${path2build}"
    echo "executables: ${executables}"

    cd ${path2build}
    make -j 128 ${executables}
    ### ---------------------------------------------------- ###
  fi
fi
