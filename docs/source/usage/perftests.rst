.. _perftests:

Running the Performance Tests
=============================

Having cloned the repository, start by building, compiling and running a test
in a build directory of your choice.

Example: Collisions0d Performance Test in Serial
------------------------------------------------
You can build and compile this example from the root of your performance_testing_cleo directory first
by building and compiling the exectuabel for a build of your choice (serial, openmp or gpu).
E.g. for a serial build:
.. code-block:: console

  $ mkdir ./build ./build/serial
  $ ./scripts/bash/build_serial.sh ./src ./build/serial
  $ ./scripts/bash/compile_cleo.sh serial ./build/serial colls0d

Then setup and run the example via:
.. code-block:: console

  $ mamba activate perftests
  $ python scripts/collisions0d/setup_colls0d_script.py /home/m/m300950/CLEO /home/m/m300950/performance_testing_cleo/build

(note you will need to change the path to `constants_filename` if you do not build in serial beforehand)
