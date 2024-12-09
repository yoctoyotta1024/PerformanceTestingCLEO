"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: use_kp_profilers.py
Project: profilers
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
classes to use Kokkos profilers in run scripts
"""

from pathlib import Path
from typing import Optional
import read_kp_profilers


def get_profiler(
    profiler: str,
    kokkos_tools_lib: Optional[Path] = Path(
        "/work/bm1183/m300950/kokkos_tools_lib/lib64/"
    ),
):
    if profiler == "none":
        return NullKpProfiler()
    elif profiler == "kerneltimer":
        return KpKernelTimer(kokkos_tools_lib)
    elif profiler == "spacetimestack":
        return KpSpaceTimeStack(kokkos_tools_lib)
    else:
        raise ValueError(f"{profiler} not a valid option. Please provide correct name.")


class NullKpProfiler:
    def __init__(self):
        print("Using No Kokkos Profiling Tool")

    def postprocess(
        self, filespath: Optional[Path] = None, to_dataset: Optional[bool] = False
    ):
        return None


class KpKernelTimer:
    def __init__(
        self,
        kokkos_tools_lib: Optional[Path] = Path(
            "/work/bm1183/m300950/kokkos_tools_lib/lib64/"
        ),
    ):
        import os

        self.kokkos_tools_lib = kokkos_tools_lib
        self.kp_reader = self.kokkos_tools_lib / ".." / "bin" / "kp_reader"

        os.environ["KOKKOS_TOOLS_LIBS"] = str(
            self.kokkos_tools_lib / "libkp_kernel_timer.so"
        )
        print("Using Kokkos Profiling Tool", os.environ["KOKKOS_TOOLS_LIBS"])
        print("Using Kokkos Tool Reader", self.kp_reader)

    def postprocess(
        self, filespath: Optional[Path] = None, to_dataset: Optional[bool] = False
    ):
        import glob
        import subprocess
        import os
        from pathlib import Path

        # Add kokkos_tools_lib to LD_LIBRARY_PATH
        ld_lib_path = os.environ.get("LD_LIBRARY_PATH", "")
        os.environ["LD_LIBRARY_PATH"] = f"{self.kokkos_tools_lib}:{ld_lib_path}"

        if filespath is None:
            filespath = Path.cwd()

        # Use glob to find all .dat files in the specified directory
        datfiles = glob.glob(os.path.join(filespath, "*.dat"))

        # Print the list of .dat files
        for filename in datfiles:
            txt_filename = str(Path(filename).with_suffix(".txt"))
            cmd = [str(self.kp_reader), filename]
            with open(txt_filename, "w") as wfile:
                subprocess.run(cmd, stdout=wfile, stderr=subprocess.STDOUT)
            if to_dataset:
                name = "KP Kernel Timer File DS"
                ds = read_kp_profilers.convert_kp_kernel_timer_to_dataset(
                    name, txt_filename
                )
                zarr_filename = str(Path(filename).name).replace(".", "p")
                zarr_filename = f"/kp_kerneltimer_{zarr_filename}.zarr"
                zarr_filename = str(Path(filename).parent) + zarr_filename
                ds.to_zarr(Path(zarr_filename))


class KpSpaceTimeStack:
    def __init__(
        self,
        kokkos_tools_lib: Optional[Path] = Path(
            "/work/bm1183/m300950/kokkos_tools_lib/lib64/"
        ),
    ):
        import os

        self.kokkos_tools_lib = kokkos_tools_lib

        os.environ["KOKKOS_TOOLS_LIBS"] = str(
            self.kokkos_tools_lib / "libkp_space_time_stack.so"
        )
        print("Using Kokkos Profiling Tool", os.environ["KOKKOS_TOOLS_LIBS"])

    def postprocess(
        self, filespath: Optional[Path] = None, to_dataset: Optional[bool] = False
    ):
        import glob
        import os

        if filespath is None:
            filespath = Path.cwd()

        # Use glob to find all .dat files in the specified directory
        datfiles = glob.glob(os.path.join(filespath, "*out.*.out"))

        for filename in datfiles:
            if to_dataset:
                name = "KP Space Time Stack File DS"
                ds = read_kp_profilers.convert_kp_space_time_stack_to_dataset(
                    name, filename
                )
                if ds is not None:
                    zarr_filename = str(Path(filename).name).replace(".", "p")
                    zarr_filename = f"/kp_spacetimestack_{zarr_filename}.zarr"
                    zarr_filename = str(Path(filename).parent) + zarr_filename
                    ds.to_zarr(Path(zarr_filename))
