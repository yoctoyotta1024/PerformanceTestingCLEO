.. _perftests:

Running the Performance Tests
=============================

Having cloned the repository, start by building, compiling and running a test
in a build directory of your choice.

Example: Collisions0d Performance Test in Serial
------------------------------------------------
You can build and compile this example from the root of your performance_testing_cleo directory first
by building and compiling the exectuabel for a build of your choice (serial, openmp or cuda).

E.g. For a serial build;
1) Build and compile:
.. code-block:: console

  $ mkdir ./builds
  $ ./scripts/bash/build_serial.sh ./src ./builds/serial
  $ ./scripts/bash/compile_cleo.sh serial ./builds/serial colls0d

2) Setup the example:
.. code-block:: console

  $ ./scripts/collisions0d/setup_colls0d.sh \
    /home/m/m300950/CLEO \
    /home/m/m300950/performance_testing_cleo \
    /home/m/m300950/performance_testing_cleo/builds \
    serial

Then you could perform one normal run with e.g.
``./builds/serial/collisions0d/colls0d ./builds/serial/tmp/colls0d/config_8_0.yaml``

Or e.g. run the example with the Kokkos kernel timer performance tool:
.. code-block:: console

  $ ./scripts/bash/run_profiling.sh \
    /home/m/m300950/performance_testing_cleo \
    /home/m/m300950/performance_testing_cleo/builds \
    colls0d \
    serial \
    kerneltimer
  $ ./scripts/bash/postproc_profiling.sh \
    /home/m/m300950/performance_testing_cleo \
    /home/m/m300950/performance_testing_cleo/builds \
    colls0d \
    serial \
    kerneltimer

Or e.g. run the example with the Kokkos kernel timer performance tool:
.. code-block:: console

  $ ./scripts/bash/run_profiling.sh \
    /home/m/m300950/performance_testing_cleo \
    /home/m/m300950/performance_testing_cleo/builds \
    colls0d \
    serial \
    spacetimestack
  $ ./scripts/bash/postproc_profiling.sh \
    /home/m/m300950/performance_testing_cleo \
    /home/m/m300950/performance_testing_cleo/builds \
    colls0d \
    serial \
    spacetimestack
