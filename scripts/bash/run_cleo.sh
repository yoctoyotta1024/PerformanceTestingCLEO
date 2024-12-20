#!/bin/bash
#SBATCH --job-name=run_cleo
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=256
#SBATCH --mem=10G
#SBATCH --time=02:00:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./run_cleo_job_out.%j.out
#SBATCH --error=./run_cleo_job_err.%j.out

### ------------------------------------------------------------------------ ###
### -------------- PLEASE NOTE: this script assumes you have --------------- ###
### -------- already built CLEO and compiled the desired executable -------- ###
### ------------------------------------------------------------------------ ###
module purge
spack unload --all

buildtype=$1
executable=$2
outpaths=($3) # execution here to puts --output and --error files there
configfiles=($4)
file_tag=$5
stacksize_limit=204800 # kB

if [[ "${buildtype}" == "" ||
      "${executable}" == "" ||
      "${outpaths}" == "" ||
      "${configfiles}" == "" ]]
then
  echo "Bad inputs, please check your buildtype, executable, outpaths and config file names"
  exit 1
fi

if [ ${#outpaths[@]} -ne ${#configfiles[@]} ]
then
  echo "Bad inputs, please check your outpaths match your config file names"
  exit 1
fi

if [[ "${buildtype}" == "cuda" ]]
then
  echo "Bad input, buildtype cannot be 'cuda'"
  exit 1
fi

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

export MALLOC_TRIM_THRESHOLD_="-1"

ulimit -s ${stacksize_limit}
ulimit -c 0

for i in "${!configfiles[@]}"; do
  echo "----- running CLEO -------"
  cd ${outpaths[$i]} && pwd
  outfile=${outpaths[$i]}/run_cleo_out.piped${file_tag}.out
  errfile=${outpaths[$i]}/run_cleo_err.piped${file_tag}.out
  runcmd="${executable} ${configfiles[$i]}"
  echo "output_file = ${outfile}"
  echo "error_file = ${errfile}"
  echo "runcmd = ${runcmd}"
  echo "$runcmd" > ${outfile} 2> ${errfile}
  eval "$runcmd" > ${outfile} 2> ${errfile}
  echo "--------------------------"
done
### ---------------------------------------------------- ###
