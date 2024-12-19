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


def open_kerneltimer_dataset(
    path2builds: Path,
    buildtype: str,
    executable: str,
    nsupers: int,
    nthreads: Optional[int] = None,
):
    import xarray as xr

    if nthreads is not None:
        path2builds = path2builds / f"builds_threads_{nthreads}"

    path2ds = (
        path2builds
        / buildtype
        / "bin"
        / executable
        / f"kp_kerneltimer_ngbxsensemble_nsupers{nsupers}.zarr"
    )
    return xr.open_zarr(path2ds)


def open_spacetimestack_dataset(
    path2builds: Path, buildtype: str, executable: str, nsupers: int
):
    import xarray as xr

    path2ds = (
        path2builds
        / buildtype
        / "bin"
        / executable
        / f"kp_spacetimestack_ngbxsensemble_nsupers{nsupers}.zarr"
    )
    return xr.open_zarr(path2ds)


def subplots(
    figsize: Optional[tuple] = (12, 18),
    nrows: Optional[int] = 1,
    ncols: Optional[int] = 1,
    sharex: Optional[bool] = False,
    sharey: Optional[bool] = False,
    logx: Optional[bool] = False,
    logy: Optional[bool] = False,
):
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes
    import numpy as np

    fig, axes = plt.subplots(
        figsize=figsize, nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey
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


def savefig(savename: Path, dpi: Optional[int] = 128):
    import matplotlib.pyplot as plt

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


def calculate_speedup(
    time: xr.DataArray,
    time_reference: xr.DataArray,
    extrapolate: Optional[bool] = False,
):
    import numpy as np

    if extrapolate:
        if time.shape != time_reference.shape or np.any(
            time.coords["ngbxs"].values != time_reference.coords["ngbxs"].values
        ):
            print("warning: speedup calculation extrapolating reference")
            time_reference = time_reference.interp(
                ngbxs=time.coords["ngbxs"], kwargs={"fill_value": "extrapolate"}
            )
    return time_reference / time


def calculate_efficiency(
    time: xr.DataArray,
    time_reference: xr.DataArray,
    buildtype: str,
    processing_units: dict,
    extrapolate: Optional[bool] = False,
):
    speedup = calculate_speedup(time, time_reference, extrapolate=extrapolate)
    return speedup / processing_units[buildtype]
