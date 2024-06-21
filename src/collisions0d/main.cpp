/*
 * Copyright (c) 2024 MPI-M, Clara Bayley
 *
 *
 * -----  PerformanceTestingCLEO -----
 * File: main.cpp
 * Project: collisions0d
 * Created Date: Friday 21st June 2024
 * Author: Clara Bayley (CB)
 * Additional Contributors:
 * -----
 * Last Modified: Friday 21st June 2024
 * Modified By: CB
 * -----
 * License: BSD 3-Clause "New" or "Revised" License
 * https://opensource.org/licenses/BSD-3-Clause
 * -----
 * File Description:
 */

#include <Kokkos_Core.hpp>
#include <iostream>

#include "zarr/fsstore.hpp"

int main(int argc, char *argv[]) {
  auto store = FSStore("/home/m/m300950/performance_testing_cleo/test.zarr");

  Kokkos::initialize(argc, argv);
  { std::cout << "Hello World\n"; }
  Kokkos::finalize();

  return 0;
}
