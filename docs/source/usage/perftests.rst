.. _perftests:

Running the Performance Tests
=============================

Having cloned the repository, start by building, compiling and running a test
in a build directory of your choice.

Example: Collisions0d Performance Test in Serial
------------------------------------------------
You can build and compile this example from your root performance_testing_cleo directory by executing
.. code-block:: console

  $ ./scripts/bash/build_serial.sh ./src ./build
  $ ./scripts/bash/compile_cleo.sh serial ./build colls0d

Then setup and run the example via:
.. code-block:: console

  $ mamba activate perftests
  $ python scripts/collisions0d/setup_colls0d_script.py /home/m/m300950/CLEO /home/m/m300950/performance_testing_cleo/build
