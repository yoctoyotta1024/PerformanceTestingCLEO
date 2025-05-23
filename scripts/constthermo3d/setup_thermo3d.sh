#!/bin/bash
#SBATCH --job-name=setup_thermo3d
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=64G
#SBATCH --time=00:10:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./setup_thermo3d_out.%j.out
#SBATCH --error=./setup_thermo3d_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

python=${1:-/work/bm1183/m300950/bin/envs/perftests/bin/python}
path2CLEO=${2:-/home/m/m300950/CLEO}
path2src=${3:-/home/m/m300950/performance_testing_cleo}       # performance_testing_cleo root dir
path2builds=${4:-${path2src}/builds}                          # builds in path2builds/[build_type]
buildtypes=("${@:5}")                                         # "serial", "openmp" , "cuda" and/or "threads"

if [ "${#buildtypes[@]}" -eq 0 ]; then
  buildtypes=("cuda" "openmp" "serial" "threads")
fi

### ----------------- run profiling --------------- ###
gen_initconds=TRUE
for buildtype in "${buildtypes[@]}"; do
  runcmd="${python} ${path2src}/scripts/constthermo3d/setup_thermo3d.py \
    ${path2CLEO} ${path2builds} ${buildtype} --gen_initconds=${gen_initconds}"
  echo ${runcmd}
  ${runcmd}
  gen_initconds=FALSE # only generate initial conditions once
done
### ---------------------------------------------------- ###
