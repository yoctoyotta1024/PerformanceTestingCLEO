#!/bin/bash
#SBATCH --job-name=run_cleo
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=256
#SBATCH --mem=10G
#SBATCH --time=00:60:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./run_cleo_out.%j.out
#SBATCH --error=./run_cleo_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

buildtype=$1
executable=$2   # get from command line argument
configfile=$3   # get from command line argument
stacksize_limit=204800 # kB

if [[ "${buildtype}" == "" ||
      "${executable}" == "" ||
      "${configfile}" == "" ]]
then
  echo "Bad inputs, please check your buildtype, executable and config file name"
else
  ### ----------------- run executable --------------- ###
  export OMPI_MCA_osc="ucx"
  export OMPI_MCA_pml="ucx"
  export OMPI_MCA_btl="self"
  export UCX_HANDLE_ERRORS="bt"
  export OMPI_MCA_pml_ucx_opal_mem_hooks=1
  export OMPI_MCA_io="romio321"          # basic optimisation of I/O
  export UCX_TLS="shm,rc_mlx5,rc_x,self" # for jobs using LESS than 150 nodes

  export OMP_PROC_BIND=spread # (!) will be overriden by KMP_AFFINITY
  export OMP_PLACES=threads # (!) will be overriden by KMP_AFFINITY
  export KMP_AFFINITY="granularity=fine,scatter" # (similar to OMP_PROC_BIND=spread)
  export KMP_LIBRARY="turnaround"

  if [[ "${buildtype}" != "cuda" ]]
  then
    export MALLOC_TRIM_THRESHOLD_="-1"

    ulimit -s ${stacksize_limit}
    ulimit -c 0
    ulimit -a

    runcmd="${executable} ${configfile}"
    echo ${runcmd}
    ${runcmd}
  fi
  ### ---------------------------------------------------- ###
fi
