#!/bin/bash
#SBATCH --job-name=grand_datasets
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem=30G
#SBATCH --time=00:10:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./grand_datasets_out.%j.out
#SBATCH --error=./grand_datasets_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

python=${1:-/work/bm1183/m300950/bin/envs/perftests/bin/python}
path2src=${2:-/home/m/m300950/performance_testing_cleo}       # performance_testing_cleo root dir
path2builds=${3:-${path2src}/builds}                          # builds in path2builds/[build_type]
executable=${4:-colls0d}
profiler=${5:-kerneltimer}                                    # "kerneltimer" or "spacetimestack"
buildtypes=("${@:6}")                                         # "serial", "openmp" and/or "cuda"

if [ "${#buildtypes[@]}" -eq 0 ]; then
  buildtypes=("cuda" "openmp" "serial")
fi

### ---------------- create grand datasets -------------- ###
for buildtype in "${buildtypes[@]}"; do
  runcmd="${python} ${path2src}/scripts/create_grand_datasets.py ${path2builds} ${buildtype} ${executable} ${profiler}"
  echo ${runcmd}
  ${runcmd}
done
### ---------------------------------------------------- ###
