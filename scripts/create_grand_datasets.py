"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: create_grand_datasets.py
Project: scripts
Created Date: Thursday 5th December 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 5th December 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script converts multiple zarr xarray datasets for nsupers and nruns of each build
type into mean over nruns for each build in one "grand" dataset.
"""

import argparse
import os
import glob
import xarray as xr
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("path2builds", type=Path, help="Absolute path to builds")
parser.add_argument(
    "buildtype", type=str, help="Type of build: serial, openmp, cuda or threads"
)
parser.add_argument("executable", type=str, help="Executable name, e.g. colls0d")
parser.add_argument("profiler", type=str, help="KP name: kerneltimer or spacetimestack")
args = parser.parse_args()

path2builds = args.path2builds
buildtype = args.buildtype
executable = args.executable
profiler = args.profiler
do_write_runs_datasets = True
nsupers_runs = {
    8: 10,
    64: 10,
    1024: 5,
    8192: 5,
    16384: 2,
    131072: 2,
    524288: 2,
}


# ---------------- function definitions ---------------- #
def find_dataset(filespath: Path, profiler: str) -> str | None:
    """returns name of zarr dataset in filespath for a given profiler if found, else returns None."""
    filenames = glob.glob(os.path.join(filespath, f"kp_{profiler}_*.zarr"))
    if filenames == []:
        msg = f"Warning: no {profiler} zarr dataset found in {filespath}"
        print(msg)
        return None
    else:
        if len(filenames) > 1:
            msg = f"Warning: only 1 of {profiler} zarr datasets found in {filespath} is being used"
            print(msg)
        return filenames[0]


def concat_datasets(ds: list[xr.Dataset], dim: str, original_files: str) -> xr.Dataset:
    if ds == []:
        msg = f"Warning: No members for grand dataset from {original_files}"
        print(msg)
        return None
    return xr.concat(ds, dim=dim)


def ensemble_over_runs_dataset(
    runs_ds: list[xr.Dataset],
    profiler: str,
    original_files: str,
    buildtype: str,
    nsupers: int,
) -> xr.Dataset | None:
    """concatenates datasets in runs_ds over new dimension "nruns"
    and adds new attributes to resulting dataset. Idea being to create a
    single dataset for an ensemble of runs of an executable for nsupers and
    a certain buildtype"""
    runs_ds = concat_datasets(runs_ds, "nrun", original_files)
    if runs_ds is None:
        return None
    runs_ds.attrs["name"] = f"KP {profiler} DS for ensemble of runs"
    del runs_ds.attrs["original_file"]
    runs_ds.attrs["original_files"] = original_files
    runs_ds.attrs["buildtype"] = buildtype
    runs_ds.attrs["nsupers"] = nsupers

    return runs_ds


def statistics_of_ensemble_over_runs_dataset(runs_ds: xr.Dataset) -> xr.Dataset:
    """returns dataset which averages over runs dimension e.g. takes mean,
    standard deviation, and lower/upper quartiles of ensemble of runs"""
    mean = runs_ds.mean(dim="nrun")
    std = runs_ds.std(dim="nrun")
    lq = runs_ds.quantile(0.25, dim="nrun", numeric_only=True).drop_vars("quantile")
    uq = runs_ds.quantile(0.75, dim="nrun", numeric_only=True).drop_vars("quantile")

    stats = [mean, std, lq, uq]
    stats_names = ["mean", "std", "lower_quartile", "upper_quartile"]
    stats_ds = xr.concat(stats, dim="statistic")
    stats_ds.coords["statistic"] = stats_names

    return stats_ds


def ensemble_over_nsupers_grand_dataset(
    grand_ds: list[xr.Dataset],
    nsupers_coord: list[int],
    profiler: str,
    original_files: str,
    buildtype: str,
) -> xr.Dataset | None:
    """concatenates datasets in grand_ds over new dimension "nsupers"
    and adds new attributes to resulting dataset. Idea being to create a
    single dataset for an ensemble of statics over runs with nsupers for
    a certain executable and buildtype"""
    grand_ds = concat_datasets(grand_ds, "nsupers", original_files)
    if grand_ds is None:
        return None
    grand_ds.coords["nsupers"] = nsupers_coord
    grand_ds.attrs["name"] = f"KP {profiler} grand DS"
    grand_ds.attrs["original_files"] = original_files
    grand_ds.attrs["buildtype"] = buildtype
    msg = (
        "grand dataset from original_files created. "
        + "Note attributes and non-float variables have been dropped"
    )
    print(msg)
    return grand_ds


# ------------------------------------------------------ #

# --------- write ensemble of runs datasets ------------ #
if do_write_runs_datasets:
    for nsupers in nsupers_runs.keys():
        runs_ds = []
        for nrun in range(nsupers_runs[nsupers]):
            filespath = (
                path2builds
                / buildtype
                / "bin"
                / executable
                / f"nsupers{nsupers}"
                / f"nrun{nrun}"
            )
            filename = find_dataset(filespath, profiler)
            if filename is not None:
                runs_ds.append(xr.open_zarr(filename))
        og_filenames = str(filespath.parent / "nrun*" / f"kp_{profiler}_*.zarr")
        runs_ds = ensemble_over_runs_dataset(
            runs_ds, profiler, og_filenames, buildtype, nsupers
        )
        if runs_ds is not None:
            filename = filespath.parent / f"kp_{profiler}_ensemble.zarr"
            runs_ds.to_zarr(filename)
# ------------------------------------------------------ #

# -------- write ensemble of nsupers datasets ---------- #
grand_ds = []
nsupers_coord = []
for nsupers in nsupers_runs.keys():
    filename = (
        path2builds
        / buildtype
        / "bin"
        / executable
        / f"nsupers{nsupers}"
        / f"kp_{profiler}_ensemble.zarr"
    )
    try:
        runs_ds = xr.open_zarr(filename)
        stats_ds = statistics_of_ensemble_over_runs_dataset(runs_ds)
        nsupers_coord.append(nsupers)
        grand_ds.append(stats_ds)
    except FileNotFoundError:
        msg = f"Warning: No data found for nsupers={nsupers} member of {filename.parent.parent} grand dataset"
        print(msg)
og_filenames = str(filename.parent.parent / "nsupers*" / filename.name)
grand_ds = ensemble_over_nsupers_grand_dataset(
    grand_ds, nsupers_coord, profiler, og_filenames, buildtype
)
if grand_ds is not None:
    filename = filename.parent.parent / f"kp_{profiler}.zarr"
    grand_ds.to_zarr(filename)
# ------------------------------------------------------ #
