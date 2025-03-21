#!/bin/bash
#SBATCH --job-name=verifycond0d
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=940M
#SBATCH --time=00:10:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./verifycond0d_out.%j.out
#SBATCH --error=./verifycond0d_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

python=${1:-/work/bm1183/m300950/bin/envs/perftests/bin/python}
path2CLEO=${2:-/home/m/m300950/CLEO}
path2src=${3:-/home/m/m300950/performance_testing_cleo} # performance_testing_cleo root dir

### info to make path2dataset, path2gridfile, dataset and setup filenames
path2builds=${4:-/work/bm1183/m300950/performance_testing_cleo/builds}
exec=${5:-cond0d}
ngbxs=${6:-1}
nsupers=${7:-128}
nthreads=${8:-1}
nrun=${9:-0}
dataset_filename=${10:-sol.zarr}
setup_filename=${11:-setup.txt}
buildtypes=("${@:12}") # "serial", "openmp" , "cuda" and/or "threads"

pythonfile="${path2src}/scripts/validations/plot_${exec}.py"
grid_filename="dimlessGBxboundaries_${ngbxs}.dat"

if [ "${#buildtypes[@]}" -eq 0 ]; then
  #buildtypes=("cuda" "openmp" "serial" "threads")
  buildtypes=("serial")
fi

### ----------------- run profiling --------------- ###
for buildtype in "${buildtypes[@]}"; do
  path2gridfile="${path2builds}/share/${exec}/${grid_filename}"
  path2data="${path2builds}/${buildtype}/bin/${exec}/ngbxs${ngbxs}_nsupers${nsupers}/nthreads${nthreads}/nrun${nrun}"
  path2dataset="${path2data}/${dataset_filename}"
  path2setupfile="${path2data}/${setup_filename}"
  runcmd="${python} ${pythonfile} ${path2CLEO} ${path2gridfile} ${path2dataset} ${path2setupfile}"
  echo ${runcmd}
  ${runcmd}
done
### ---------------------------------------------------- ###
