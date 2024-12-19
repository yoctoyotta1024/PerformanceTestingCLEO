"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: strong_scaling.py
Project: plotting
Created Date: Monday 9th December 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Monday 9th December 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script for plotting strong scaling results (increasing reesources for fixed problem size)
from zarr xarray datasets for kokkos profiling data. Note: standard data format assumed.
"""

# %%
import argparse
import numpy as np
from pathlib import Path
import sys

path2src = Path(__file__).resolve().parent.parent.parent / "src"
sys.path.append(str(path2src))  # for imports for input files generation
from plotting import helperfuncs as hfuncs

# e.g. ipykernel_launcher.py [path2builds] [executable]
parser = argparse.ArgumentParser()
parser.add_argument(
    "--path2builds",
    type=Path,
    help="Absolute path to builds",
    default="/work/bm1183/m300950/performance_testing_cleo/thirdattempt_strongscaling",
)
parser.add_argument(
    "--executable",
    type=str,
    choices=["colls0d"],
    help="Executable name, e.g. colls0d",
    default="colls0d",
)
args, unknown = parser.parse_known_args()
path2builds = args.path2builds
executable = args.executable

buildtypes = ["serial", "openmp", "threads", "cuda"]

nthreads = [1, 8, 16, 64, 128, 256]

ngbxs_nsupers_runs = {
    (4096, 16): 1,
    (8192, 16): 1,
    (16384, 16): 1,
    (262144, 16): 1,
}

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")


# %% funtion definitions for strong scaling plots
def plot_strong_scaling(
    path2builds: Path,
    buildtypes: list[str],
    executable: str,
    ngbxs_nsupers_runs: dict,
    nthreads2plt: list[int],
):
    fig, axs = hfuncs.subplots(figsize=(12, 8), logx=True, logy=True)

    for buildtype in buildtypes:
        for ngbx, nsupers in ngbxs_nsupers_runs.keys():
            x, yarr = [], []
            for nthreads in nthreads2plt:
                try:
                    dataset = hfuncs.open_kerneltimer_dataset(
                        path2builds, buildtype, executable, nsupers, nthreads=nthreads
                    )
                except FileNotFoundError:
                    msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers}, nthreads={nthreads}"
                    print(msg)
                    continue
                try:
                    tottime = dataset.summary.sel(ngbxs=ngbx)[:, 0]
                except KeyError:
                    msg = f"warning: skipping buildtype={buildtype} ngbxs={ngbx}, nsupers={nsupers}, nthreads={nthreads}"
                    print(msg)
                    continue
                x.append(nthreads)
                yarr.append(tottime)
            if x != []:
                x = np.asarray(x)
                yarr = np.asarray(yarr)
                y = yarr[:, 0]
                lq = yarr[:, 2]
                uq = yarr[:, 3]
                lab = buildtype
                c = "k"
                axs.plot(
                    x,
                    y,
                    color=c,
                    marker=markers[lab],
                    linestyle=lstyles[lab],
                    label=lab,
                )
                hfuncs.add_shading(axs, x, lq, uq, c, lstyles[lab])
    axs.legend()
    axs.set_xlabel("number of CPU threads")
    axs.set_ylabel("speedup")
    return fig, axs


# %%
fig, axs = plot_strong_scaling(
    path2builds, buildtypes, executable, ngbxs_nsupers_runs, nthreads
)
savename = savedir / "strong_scaling_summary.png"
hfuncs.savefig(savename)

# %%
