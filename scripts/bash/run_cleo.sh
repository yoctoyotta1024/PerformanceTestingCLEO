#!/bin/bash
#SBATCH --job-name=run_cleo
#SBATCH --partition=gpu
#SBATCH --gpus=4
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --mem=30G
#SBATCH --time=00:30:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=/home/m/m300950/performance_testing_cleo/run_cleo_out.%j.out
#SBATCH --error=/home/m/m300950/performance_testing_cleo/run_cleo_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

executable=$1   # get from command line argument
configfile=$2   # get from command line argument

if [[ "${executable}" == "" ||
      "${configfile}" == "" ]]
then
  echo "Bad inputs, please check your executable and config file name"
else
  ### ----------------- run executable --------------- ###
  # TODO(CB): use performance suitable omp threads and compiler flags etc. before running
  export OMP_PROC_BIND=spread
  export OMP_PLACES=threads

  runcmd="${executable} ${configfile}"
  echo ${runcmd}
  ${runcmd}
  ### ---------------------------------------------------- ###
fi
