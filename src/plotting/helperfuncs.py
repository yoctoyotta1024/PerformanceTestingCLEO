"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: helperfuncs.py
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
functions / classes to help scripts which load and plot performance data
"""

from pathlib import Path
from typing import Optional
import xarray as xr

buildtype_lstyles = {
    "serial": "dotted",
    "openmp": "dashdot",
    "cuda": "solid",
    "threads": "dashed",
}

buildtype_markers = {"serial": "o", "openmp": "s", "cuda": "x", "threads": "d"}


def get_grand_dataset_name(
    binpath: Path, profiler: str, ensembletype: str, n: int
) -> Path:
    if ensembletype == "gbxs":
        return binpath / f"kp_{profiler}_ngbxsensemble_nsupers{n}.zarr"
    elif ensembletype == "supers":
        return binpath / f"kp_{profiler}_ngbxs{n}_nsupersensemble.zarr"
    else:
        raise ValueError("unknown ensemble type, please choose 'gbxs' or 'supers'")


def open_kerneltimer_dataset(
    path2builds: Path,
    buildtype: str,
    executable: str,
    ensembletype: str,
    n: int,
):
    import xarray as xr

    binpath = path2builds / buildtype / "bin" / executable
    path2ds = get_grand_dataset_name(binpath, "kerneltimer", ensembletype, n)
    return xr.open_zarr(path2ds)


def open_spacetimestack_dataset(
    path2builds: Path, buildtype: str, executable: str, ensembletype: str, n: int
):
    import xarray as xr

    binpath = path2builds / buildtype / "bin" / executable
    path2ds = get_grand_dataset_name(binpath, "spacetimestack", ensembletype, n)
    return xr.open_zarr(path2ds)


def subplots(
    figsize: Optional[tuple] = (12, 18),
    nrows: Optional[int] = 1,
    ncols: Optional[int] = 1,
    sharex: Optional[bool] = False,
    sharey: Optional[bool] = False,
    logx: Optional[bool] = False,
    logy: Optional[bool] = False,
    hratios: Optional[list[float]] = None,
    wratios: Optional[list[float]] = None,
):
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    import numpy as np

    fig, axes = plt.subplots(
        figsize=figsize,
        nrows=nrows,
        ncols=ncols,
        sharex=sharex,
        sharey=sharey,
        height_ratios=hratios,
        width_ratios=wratios,
    )

    if isinstance(axes, Axes):
        axs = np.array([axes])
    else:
        axs = axes

    for ax in axs.flatten():
        ax.spines[["right", "top"]].set_visible(False)

    if logx:
        for ax in axs.flatten():
            ax.set_xscale("log")
    if logy:
        for ax in axs.flatten():
            ax.set_yscale("log")

    return fig, axes


def savefig(savename: Path, dpi: Optional[int] = 128, tight: Optional[bool] = True):
    import matplotlib.pyplot as plt

    if tight:
        plt.tight_layout()

    plt.savefig(savename, dpi=dpi, bbox_inches="tight")
    print(f"figure saved as {str(savename)}")


def add_shading(
    ax,
    x,
    lower,
    upper,
    c,
    ls,
    a: Optional[float] = 0.3,
    label: Optional[str] = None,
    add_y: Optional[bool] = None,
):
    if add_y is not None:
        lower = add_y - lower
        upper = add_y + upper
    ax.fill_between(
        x, lower, upper, color=c, linestyle=ls, alpha=a, label=label, zorder=0
    )


def extrapolate_ngbxs_coord(data, new_ngbxs):
    extrapolated = data.interp(ngbxs=new_ngbxs, kwargs={"fill_value": "extrapolate"})
    return extrapolated


def extrapolate_nsupers_coord(data, new_nsupers):
    extrapolated = data.interp(
        nsupers=new_nsupers, kwargs={"fill_value": "extrapolate"}
    )
    return extrapolated


def calculate_speedup(
    time: xr.DataArray,
    time_reference: xr.DataArray,
    extrapolate: Optional[bool] = False,
    coord: Optional[str] = None,
):
    import numpy as np

    if extrapolate:
        if time.shape != time_reference.shape or np.any(
            time.coords[coord].values != time_reference.coords[coord].values
        ):
            print("warning: speedup calculation extrapolating reference")
            if coord == "ngbxs":
                time_reference = extrapolate_ngbxs_coord(
                    time_reference, time.coords["ngbxs"]
                )
            elif coord == "nsupers":
                time_reference = extrapolate_nsupers_coord(
                    time_reference, time.coords["nsupers"]
                )
            else:
                raise ValueError(
                    f"No extraploation function provided for coord={coord}"
                )

    return time_reference / time


def calculate_efficiency(
    time: xr.DataArray,
    time_reference: xr.DataArray,
    num_processing_units: dict,
    extrapolate: Optional[bool] = False,
    coord: Optional[str] = None,
):
    speedup = calculate_speedup(
        time, time_reference, extrapolate=extrapolate, coord=coord
    )
    return speedup / num_processing_units
