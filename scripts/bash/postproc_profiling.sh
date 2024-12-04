#!/bin/bash
#SBATCH --job-name=postproc_profiling
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=30G
#SBATCH --time=00:10:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./postproc_prof_out.%j.out
#SBATCH --error=./postproc_prof_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

path2src=${1:-/home/m/m300950/performance_testing_cleo}       # performance_testing_cleo root dir
path2builds=${2:-${path2src}/builds}                          # builds in path2builds/[build_type]
executable=${3:-colls0d}
buildtype=${4:-serial}                                        # "serial", "openmp" or "gpu"
profiler=${5:-kerneltimer}                                    # "kerneltimer" or "spacetimestack"
python=${6:-/work/bm1183/m300950/bin/envs/perftests/bin/python}

### ----------------- run profiling --------------- ###
runcmd="${python} ${path2src}/scripts/postproc_profiling.py ${path2builds} ${buildtype} ${executable} ${profiler}"
echo ${runcmd}
${runcmd}
### ---------------------------------------------------- ###