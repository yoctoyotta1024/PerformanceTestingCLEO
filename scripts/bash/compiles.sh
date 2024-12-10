#!/bin/bash
#SBATCH --job-name=compileexec
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=1
#SBATCH --mem=30G
#SBATCH --time=00:10:00
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
module purge
spack unload --all

path2builds=$1     # get from command line argument
executable=$2      # get from command line argument
buildtypes=("${@:3}")      # get from command line argument

for buildtype in "${buildtypes[@]}"; do
    if [ "${buildtype}" != "serial" ] && [ "${buildtype}" != "openmp" ] && [ "${buildtype}" != "cuda" ] && [ "${buildtype}" != "threads" ];
    then
        echo "'${buildtype}' not valid build type. Please specify 'serial', 'openmp', 'cuda' or 'threads'"
    fi
    if [ "${buildtype}" == "serial" ] || [ "${buildtype}" == "openmp" ] || [ "${buildtype}" == "cuda" ] || [ "${buildtype}" == "threads" ];
    then
        ### ------------------- load packages ------------------ ###
        module load gcc/11.2.0-gcc-11.2.0 openmpi/4.1.2-gcc-11.2.0 # use gcc mpi wrappers
        spack load cmake@3.23.1%gcc
        # load nvhpc compilers if compiling cuda build
        if [[ "${buildtype}" == "cuda" ]]
        then
            module load nvhpc/23.9-gcc-11.2.0
        fi
        ### ---------------- compile executables --------------- ###
        path2build=${path2builds}/${buildtype}
        echo "path to build directory: ${path2build}"
        echo "executable: ${executable}"

        make -C ${path2build} -j 128 ${executable}
        ### ---------------------------------------------------- ###
    fi
done
