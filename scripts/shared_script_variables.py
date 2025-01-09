"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: shared_script_variables.py
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
Script defining variables/functions that are common between
various other scripts in this project
"""

from pathlib import Path
from typing import Optional


def get_ngbxs_nsupers_runs() -> dict:
    ngbxs_nsupers_runs = {
        (1, 8): 5,
        (16, 8): 5,
        (64, 8): 5,
        (128, 8): 5,
        (256, 8): 5,
        (512, 8): 5,
        (1024, 8): 5,
        (2048, 8): 5,
        (4096, 8): 5,
        (8192, 8): 5,
        (16384, 8): 5,
        (32768, 8): 5,
    }
    return ngbxs_nsupers_runs


def get_ngbxs_nsupers_nthreads(
    buildtype: str, ngbxs_nsupers_runs: Optional[str] = None
) -> dict:
    if buildtype == "serial":
        ngbxs_nsupers_nthreads = {
            (ngbxs, nsupers): [1] for ngbxs, nsupers in ngbxs_nsupers_runs.keys()
        }
    else:
        ngbxs_nsupers_nthreads = {
            (1, 8): [256, 128, 64, 16, 8, 1],
            (16, 8): [256, 128, 64, 16, 8, 1],
            (64, 8): [256, 128, 64, 16, 8, 1],
            (128, 8): [256, 128, 64, 16, 8, 1],
            (256, 8): [256, 128, 64, 16, 8, 1],
            (512, 8): [256, 128, 64, 16, 8],
            (1024, 8): [256, 128, 64, 16, 8],
            (2048, 8): [256, 128, 64, 16, 8],
            (4096, 8): [256, 128, 64, 16, 8],
            (8192, 8): [256, 128, 64, 16, 8],
            (16384, 8): [256, 128, 64, 16, 8],
            (32768, 8): [256, 128, 64, 16, 8],
        }
    return ngbxs_nsupers_nthreads


def get_config_filename(
    tmppath: Path, ngbxs: int, nsupers: int, nrun: int, nthreads: Optional[int] = None
) -> Path:
    if nthreads is not None:
        return tmppath / f"config_{ngbxs}_{nsupers}_{nthreads}_{nrun}.yaml"
    else:
        return tmppath / f"config_{ngbxs}_{nsupers}_{nrun}.yaml"


def get_all_nthreads_config_filenames(
    path2build: Path,
    executable: str,
    ngbxs: int,
    nsupers: int,
    nrun: int,
    all_nthreads: Optional[list[int]] = [None],
) -> list[Path]:
    tmppath = path2build / "tmp" / executable
    configfiles = []
    for nthreads in all_nthreads:
        file = get_config_filename(tmppath, ngbxs, nsupers, nrun, nthreads=nthreads)
        configfiles.append(file)
    return configfiles


def get_run_binpath(
    binpath: Path, ngbxs: int, nsupers: int, nrun: int, nthreads: Optional[int] = None
) -> Path:
    if nthreads is not None:
        return (
            binpath
            / f"ngbxs{ngbxs}_nsupers{nsupers}"
            / f"nthreads{nthreads}"
            / f"nrun{nrun}"
        )
    else:
        return binpath / f"ngbxs{ngbxs}_nsupers{nsupers}" / f"nrun{nrun}"


def get_all_nthreads_run_binpaths(
    path2build: Path,
    executable: str,
    ngbxs: int,
    nsupers: int,
    nrun: int,
    all_nthreads: Optional[list[int]] = [None],
) -> list[Path]:
    binpath = path2build / "bin" / executable
    paths = []
    for nthreads in all_nthreads:
        binpath_run = get_run_binpath(binpath, ngbxs, nsupers, nrun, nthreads=nthreads)
        paths.append(binpath_run)
    return paths


def get_runsensemblestats_dataset_name(
    binpath: Path,
    ngbxs: int,
    nsupers: int,
    profiler: str,
    nthreads: Optional[int] = None,
) -> Path:
    if nthreads is not None:
        return (
            binpath
            / f"ngbxs{ngbxs}_nsupers{nsupers}"
            / f"nthreads{nthreads}"
            / f"kp_{profiler}_runsensemblestats.zarr"
        )
    else:
        return (
            binpath
            / f"ngbxs{ngbxs}_nsupers{nsupers}"
            / f"kp_{profiler}_runsensemblestats.zarr"
        )


def get_grand_dataset_name(binpath: Path, nsupers: int, profiler: str) -> Path:
    return binpath / f"kp_{profiler}_ngbxsensemble_nsupers{nsupers}.zarr"
