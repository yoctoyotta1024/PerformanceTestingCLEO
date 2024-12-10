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
#. Build and compile:

   .. code-block:: console

     $ mkdir /work/bm1183/m300950/performance_testing_cleo/builds
     $ ./scripts/bash/builds.sh ./src /work/bm1183/m300950/performance_testing_cleo/builds serial openmp cuda
     $ ./scripts/bash/compiles.sh /work/bm1183/m300950/performance_testing_cleo/builds colls0d serial openmp cuda

#. Setup the example:

   .. code-block:: console

     $ ./scripts/collisions0d/setup_colls0d.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/CLEO \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       serial openmp cuda

#. a) Then you could perform one normal run with e.g.
``./builds/serial/collisions0d/colls0d ./builds/serial/tmp/colls0d/config_8_0.yaml``

#. b) Or e.g. run the example with the Kokkos kernel timer performance tool:

   .. code-block:: console

    $ ./scripts/bash/run_profiling.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      colls0d \
      kerneltimer \
      sbatch \
      serial openmp cuda
    $ ./scripts/bash/postproc_profiling.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      colls0d \
      kerneltimer \
      serial openmp cuda

#. c) Or e.g. run the example with the Kokkos kernel timer performance tool:

   .. code-block:: console

     $ ./scripts/bash/run_profiling.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       colls0d \
       spacetimestack \
       sbatch \
       serial openmp cuda
     $ ./scripts/bash/postproc_profiling.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       colls0d \
       spacetimestack \
       serial openmp cuda

#. Then concatenate runs into single dataset for each build e.g. using helper script

   .. code-block:: console

     $ ./scripts/bash/create_grand_datasets.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       colls0d \
       kerneltimer \
       serial openmp cuda
     $ ./scripts/bash/create_grand_datasets.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       colls0d \
       spacetimestack \
       serial openmp cuda
