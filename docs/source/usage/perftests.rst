.. _perftests:

Running the Performance Tests
=============================

Having cloned the repository, start by building, compiling and running a test
in a build directory of your choice.

Example: Collisions0d Performance Test in Serial
------------------------------------------------
You can build and compile this example from the root of your performance_testing_cleo directory first
by building and compiling the exectuabel for a build of your choice (serial, openmp or gpu).

E.g. For a serial build;
1) Build and compile:
.. code-block:: console

  $ mkdir ./builds
  $ ./scripts/bash/build_serial.sh ./src ./builds/serial
  $ ./scripts/bash/compile_cleo.sh serial ./builds/serial colls0d

2) Setup the example:
.. code-block:: console

  $ mamba activate perftests
  $ python scripts/collisions0d/setup_colls0d.py /home/m/m300950/CLEO /home/m/m300950/performance_testing_cleo/builds serial

Then you could perform one normal run with e.g.
``./builds/serial/collisions0d/colls0d ./builds/serial/tmp/colls0d/config_8_0.yaml``

Or e.g. run the example with the Kokkos kernel timer performance tool:
.. code-block:: console

  $ python scripts/collisions0d/run_colls0d.py /home/m/m300950/performance_testing_cleo/builds/ serial kerneltimer
  $ python scripts/collisions0d/postproc_colls0d.py /home/m/m300950/performance_testing_cleo/builds/ serial kerneltimer

Or e.g. run the example with the Kokkos kernel timer performance tool:
.. code-block:: console

  $ python scripts/collisions0d/run_colls0d.py /home/m/m300950/performance_testing_cleo/builds/ serial spacetimestack
  $ python scripts/collisions0d/postproc_colls0d.py /home/m/m300950/performance_testing_cleo/builds/ serial spacetimestack

# TODO(CB): update with correct way to use profilers
