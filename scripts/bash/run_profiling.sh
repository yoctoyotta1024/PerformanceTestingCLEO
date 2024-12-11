#!/bin/bash
#SBATCH --job-name=run_profiling
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=940M
#SBATCH --time=00:05:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./run_prof_out.%j.out
#SBATCH --error=./run_prof_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

python=${1:-/work/bm1183/m300950/bin/envs/perftests/bin/python}
path2src=${2:-/home/m/m300950/performance_testing_cleo}       # performance_testing_cleo root dir
path2builds=${3:-${path2src}/builds}                          # builds in path2builds/[build_type]
executable=${4:-collisions0d/colls0d}
profiler=${5:-kerneltimer}                                    # "kerneltimer" or "spacetimestack"
sbatch=${6:-sbatch}                                           # "sbatch" or otherwise false
buildtypes=("${@:7}")                                         # "serial", "openmp" , "cuda" and/or "threads"

if [ "${#buildtypes[@]}" -eq 0 ]; then
  buildtypes=("cuda" "openmp" "serial" "threads")
fi

### ----------------- run profiling --------------- ###
for buildtype in "${buildtypes[@]}"; do
  runcmd="${python} ${path2src}/scripts/run_profiling.py ${path2builds} ${buildtype} ${executable} ${profiler} ${sbatch}"
  echo ${runcmd}
  ${runcmd}
done
### ---------------------------------------------------- ###
