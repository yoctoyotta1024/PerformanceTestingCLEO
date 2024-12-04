#!/bin/bash
#SBATCH --job-name=setup_colls0d
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=30G
#SBATCH --time=00:10:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./setup_colls0d_out.%j.out
#SBATCH --error=./setup_colls0d_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

path2CLEO=${1:-/home/m/m300950/CLEO}
path2src=${2:-/home/m/m300950/performance_testing_cleo}       # performance_testing_cleo root dir
path2builds=${3:-${path2src}/builds}                          # builds in path2builds/[build_type]
buildtype=${4:-serial}                                        # "serial", "openmp" or "gpu"
python=${5:-/work/bm1183/m300950/bin/envs/perftests/bin/python}

### ----------------- run profiling --------------- ###
runcmd="${python} ${path2src}/scripts/collisions0d/setup_colls0d.py ${path2CLEO} ${path2builds} ${buildtype}"
echo ${runcmd}
${runcmd}
### ---------------------------------------------------- ###
