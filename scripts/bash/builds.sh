#!/bin/bash
#SBATCH --job-name=builds
#SBATCH --partition=compute
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=30G
#SBATCH --time=00:05:00
#SBATCH --mail-user=clara.bayley@mpimet.mpg.de
#SBATCH --mail-type=FAIL
#SBATCH --account=bm1183
#SBATCH --output=./build/bin/builds_out.%j.out
#SBATCH --error=./build/bin/builds_err.%j.out


path2src=$1      # required
path2builds=$2   # required
buildtypes=("${@:3}")

path2buildbash=${path2src}/../scripts/bash/

for buildtype in "${buildtypes[@]}"; do
    ### --------------------- build source ------------------- ###
    if [ "${buildtype}" != "serial" ] && [ "${buildtype}" != "openmp" ] && [ "${buildtype}" != "cuda" ] && [ "${buildtype}" != "threads" ] ;
    then
        echo "'${buildtype}' not valid build type. Please specify 'serial', 'openmp', 'cuda' or 'threads'"
    fi
    if [ "${buildtype}" == "serial" ] || [ "${buildtype}" == "openmp" ] || [ "${buildtype}" == "cuda" ] || [ "${buildtype}" == "threads" ];
    then
        buildbash=${path2buildbash}/build_${buildtype}.sh
        path2build=${path2builds}/${buildtype}
        echo "build type: ${buildtype}"
        echo "path to src: ${path2src}"
        echo "path to build directories: ${path2build}"
        echo "${buildbash} ${path2src} ${path2build}"
        ${buildbash} ${path2src} ${path2build} ${enableyac} ${yacyaxtroot}
    fi
done
