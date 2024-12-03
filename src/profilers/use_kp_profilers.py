"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: use_kp_profilers.py
Project: profilers
Created Date: Monday 24th June 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Monday 24th June 2024
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


class KpKernelTimer:
    def __init__(
        self,
        kokkos_tools_lib: Optional[Path] = Path(
            "/work/bm1183/m300950/kokkos_tools_lib/lib64/"
        ),
    ):
        import os

        os.environ["KOKKOS_TOOLS_LIBS"] = str(
            kokkos_tools_lib / "libkp_kernel_timer.so"
        )
        print("Using Kokkos Profiling Tool", os.environ["KOKKOS_TOOLS_LIBS"])

    def postprocess(self):
        print("now convert to zarr WIP")  # TODO(CB): finish


class KpSpaceTimeStack:
    def __init__(
        self,
        kokkos_tools_lib: Optional[Path] = Path(
            "/work/bm1183/m300950/kokkos_tools_lib/lib64/"
        ),
    ):
        import os

        os.environ["KOKKOS_TOOLS_LIBS"] = str(
            kokkos_tools_lib / "libkp_space_time_stack.so"
        )
        print("Using Kokkos Profiling Tool", os.environ["KOKKOS_TOOLS_LIBS"])

    def postprocess(self):
        print("now convert to zarr WIP")  # TODO(CB): finish


# TODO(CB): likewise for memory profiler
