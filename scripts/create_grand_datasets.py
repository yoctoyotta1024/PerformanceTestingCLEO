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
import sys
import xarray as xr
from pathlib import Path
from typing import Optional

import shared_script_variables as ssv

path2src = Path(__file__).resolve().parent.parent / "src"
sys.path.append(str(path2src))  # for helperfuncs module
from plotting import helperfuncs as hfuncs

parser = argparse.ArgumentParser()
parser.add_argument("path2builds", type=Path, help="Absolute path to builds")
parser.add_argument(
    "buildtype",
    type=str,
    choices=["serial", "openmp", "cuda", "threads"],
    help="Type of build: serial, openmp, cuda or threads",
)
parser.add_argument(
    "executable",
    type=str,
    choices=["colls0d", "thermo3d"],
    help="Executable name, e.g. colls0d",
)
parser.add_argument(
    "profiler",
    type=str,
    choices=["kerneltimer", "spacetimestack"],
    help="KP name: kerneltimer or spacetimestack",
)
parser.add_argument(
    "--allow_overwrite",
    type=str,
    choices=["TRUE", "FALSE"],
    default="FALSE",
    help="Allow zarr datasets to overwrite exisiting ones (!)",
)
args = parser.parse_args()

path2build = args.path2builds / args.buildtype
buildtype = args.buildtype
executable = args.executable
profiler = args.profiler
do_write_runs_datasets = True
do_write_grand_gbxs_dataset = False
do_write_grand_supers_dataset = True
if args.allow_overwrite == "TRUE":
    allow_overwrite = True
else:
    allow_overwrite = False
binpath = path2build / "bin" / executable

nsupers_grand_gbxs_datasets = []
ngbxs_grand_supers_datasets = [1]

ngbxs_nsupers_runs = ssv.get_ngbxs_nsupers_runs()
ngbxs_nsupers_nthreads = ssv.get_ngbxs_nsupers_nthreads(
    buildtype, ngbxs_nsupers_runs=ngbxs_nsupers_runs
)


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


def concat_datasets(
    ds: list[xr.Dataset],
    dim: str,
    original_files: str,
    match_attrs: Optional[dict] = None,
) -> xr.Dataset:
    if ds == []:
        msg = f"Warning: No members for grand dataset from {original_files}"
        print(msg)
        return None

    if match_attrs is not None:
        for attr, values in match_attrs.items():
            for d in ds:
                assert d.attrs[attr] == values
    ds = xr.concat(ds, dim=dim)

    return ds


def ensemble_over_runs_dataset(
    runs_ds: list[xr.Dataset],
    profiler: str,
    original_files: str,
    buildtype: str,
    nsupers: int,
    ngbxs: int,
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
    runs_ds.attrs["ngbxs"] = ngbxs

    return runs_ds


def statistics_of_ensemble_over_runs_dataset(runs_ds: xr.Dataset) -> xr.Dataset:
    """returns dataset which averages over runs dimension e.g. takes mean,
    standard deviation, and lower/upper quartiles of ensemble of runs"""
    mean = runs_ds.mean(dim="nrun", keep_attrs=True)
    std = runs_ds.std(dim="nrun")
    lq = runs_ds.quantile(0.25, dim="nrun", numeric_only=True).drop_vars("quantile")
    uq = runs_ds.quantile(0.75, dim="nrun", numeric_only=True).drop_vars("quantile")

    stats = [mean, std, lq, uq]
    stats_names = ["mean", "std", "lower_quartile", "upper_quartile"]
    stats_ds = xr.concat(stats, dim="statistic")
    stats_ds.coords["statistic"] = stats_names

    del stats_ds.attrs["name"]
    stats_ds.attrs["name"] = f"KP {profiler} DS for statistics over ensemble of runs"

    msg = "dataset for statistics over nruns created. Note: non-float variables have been dropped"
    print(msg)

    return stats_ds


def ensemble_grand_dataset_over_coord(
    grand_ds: list[xr.Dataset],
    coord_name: str,
    coord_values: list[int],
    profiler: str,
    original_files: str,
    buildtype: str,
    match_attrs: Optional[dict] = None,
    del_attrs: Optional[list[str]] = None,
) -> xr.Dataset | None:
    """concatenates datasets in grand_ds over new dimension "nsupers"
    and adds new attributes to resulting dataset. Idea being to create a
    single dataset for an ensemble of statics over runs with nsupers for
    a certain executable and buildtype"""
    grand_ds = concat_datasets(grand_ds, coord_name, original_files, match_attrs)
    if grand_ds is None:
        return None
    grand_ds.coords[coord_name] = coord_values
    grand_ds.attrs["name"] = f"KP {profiler} grand DS over {coord_name}"
    grand_ds.attrs["original_files"] = original_files
    grand_ds.attrs["buildtype"] = buildtype

    if del_attrs is not None:
        for attr in del_attrs:
            del grand_ds.attrs[attr]
    msg = f"grand dataset for statistics over nruns for various {coord_name} created."
    print(msg)
    return grand_ds


def write_zarr_dataset(ds: xr.Dataset, zarr_filename: Path, allow_overwrite: bool):
    if allow_overwrite:
        mode = "w"
    else:
        mode = "w-"
    ds.to_zarr(zarr_filename, mode=mode)


# ------------------------------------------------------ #


# --------- write ensemble of runs datasets ------------ #
if do_write_runs_datasets:
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        for nthreads in ngbxs_nsupers_nthreads[(ngbxs, nsupers)]:
            runs_ds = []
            for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
                filespath = ssv.get_run_binpath(
                    binpath, ngbxs, nsupers, nrun, nthreads=nthreads
                )
                filename = find_dataset(filespath, profiler)
                if filename is not None:
                    runs_ds.append(xr.open_zarr(filename))
            og_filenames = str(filespath.parent / "nrun*" / f"kp_{profiler}_*.zarr")
            runs_ds = ensemble_over_runs_dataset(
                runs_ds, profiler, og_filenames, buildtype, nsupers, ngbxs
            )
            if runs_ds is not None:
                filename = ssv.get_runsensemblestats_dataset_name(
                    binpath, ngbxs, nsupers, profiler, nthreads=nthreads
                )
                write_zarr_dataset(runs_ds, filename, allow_overwrite)
# ------------------------------------------------------ #

# -------- write ensemble of ngbxs datasets ---------- #
if do_write_grand_gbxs_dataset:
    for nsupers_dataset in nsupers_grand_gbxs_datasets:
        grand_ds = []
        ngbxs_values = []
        for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
            nthreads_ds = []
            nthreads_values = []
            for nthreads in ngbxs_nsupers_nthreads[(ngbxs, nsupers)]:
                if nsupers == nsupers_dataset:
                    filename = ssv.get_runsensemblestats_dataset_name(
                        binpath, ngbxs, nsupers_dataset, profiler, nthreads=nthreads
                    )
                    try:
                        runs_ds = xr.open_zarr(filename)
                        stats_ds = statistics_of_ensemble_over_runs_dataset(runs_ds)
                        nthreads_values.append(nthreads)
                        nthreads_ds.append(stats_ds)
                    except FileNotFoundError:
                        msg = (
                            f"Warning: No data found for ngbxs={ngbxs},"
                            + f" nthreads={nthreads} member of {filename.parent.parent}"
                            + f" nsupers={nsupers_dataset} grand dataset"
                        )
                        print(msg)
                else:
                    msg = f"skipping ngbxs={ngbxs} nthreads={nthreads} nsupers={nsupers}, not member of this grand dataset"
                    print(msg)

            og_filenames = str(
                filename.parent.parent
                / f"ngbxs{ngbxs}_nsupers{nsupers_dataset}"
                / "ntheads*"
                / filename.name
            )
            nthreads_ds = ensemble_grand_dataset_over_coord(
                nthreads_ds,
                "nthreads",
                nthreads_values,
                profiler,
                og_filenames,
                buildtype,
                match_attrs={"nsupers": nsupers_dataset, "ngbxs": ngbxs},
            )
            if nthreads_ds is not None:
                ngbxs_values.append(ngbxs)
                grand_ds.append(nthreads_ds)

        og_filenames = str(
            filename.parent.parent
            / f"ngbxs*_nsupers{nsupers_dataset}"
            / "ntheads*"
            / filename.name
        )
        grand_ds = ensemble_grand_dataset_over_coord(
            grand_ds,
            "ngbxs",
            ngbxs_values,
            profiler,
            og_filenames,
            buildtype,
            match_attrs={"nsupers": nsupers_dataset},
            del_attrs=["ngbxs"],
        )
        if grand_ds is not None:
            filename = hfuncs.get_grand_dataset_name(
                binpath, profiler, "gbxs", nsupers_dataset
            )
            print(grand_ds)
            write_zarr_dataset(grand_ds, filename, allow_overwrite)
# ------------------------------------------------------ #

# -------- write ensemble of superdrops per gridbox datasets ---------- #
if do_write_grand_supers_dataset:
    for ngbxs_dataset in ngbxs_grand_supers_datasets:
        grand_ds = []
        nsupers_values = []
        for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
            nthreads_ds = []
            nthreads_values = []
            for nthreads in ngbxs_nsupers_nthreads[(ngbxs, nsupers)]:
                if ngbxs == ngbxs_dataset:
                    filename = ssv.get_runsensemblestats_dataset_name(
                        binpath, ngbxs_dataset, nsupers, profiler, nthreads=nthreads
                    )
                    try:
                        runs_ds = xr.open_zarr(filename)
                        stats_ds = statistics_of_ensemble_over_runs_dataset(runs_ds)
                        nthreads_values.append(nthreads)
                        nthreads_ds.append(stats_ds)
                    except FileNotFoundError:
                        msg = (
                            f"Warning: No data found for nsupers={nsupers},"
                            + f" nthreads={nthreads} member of {filename.parent.parent}"
                            + f" ngbxs={ngbxs_dataset} grand dataset"
                        )
                        print(msg)
                else:
                    msg = f"skipping nsupers={nsupers} nthreads={nthreads} ngbxs={ngbxs}, not member of this grand dataset"
                    print(msg)

            og_filenames = str(
                filename.parent.parent
                / f"ngbxs{ngbxs_dataset}_nsupers{nsupers}"
                / "ntheads*"
                / filename.name
            )
            nthreads_ds = ensemble_grand_dataset_over_coord(
                nthreads_ds,
                "nthreads",
                nthreads_values,
                profiler,
                og_filenames,
                buildtype,
                match_attrs={"nsupers": nsupers, "ngbxs": ngbxs_dataset},
            )
            if nthreads_ds is not None:
                nsupers_values.append(nsupers)
                grand_ds.append(nthreads_ds)

        og_filenames = str(
            filename.parent.parent
            / f"ngbxs{ngbxs_dataset}_nsupers*"
            / "ntheads*"
            / filename.name
        )
        grand_ds = ensemble_grand_dataset_over_coord(
            grand_ds,
            "nsupers",
            nsupers_values,
            profiler,
            og_filenames,
            buildtype,
            match_attrs={"ngbxs": ngbxs_dataset},
            del_attrs=["nsupers"],
        )
        if grand_ds is not None:
            filename = hfuncs.get_grand_dataset_name(
                binpath, profiler, "supers", ngbxs_dataset
            )
            print(grand_ds)
            write_zarr_dataset(grand_ds, filename, allow_overwrite)
# ------------------------------------------------------ #
