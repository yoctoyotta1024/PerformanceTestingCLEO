.. _perftests:

Running the Performance Tests
=============================

Having cloned the repository, start by building, compiling and running a test
in a build directory of your choice.

Example: Collisions0d Performance Test in Serial
------------------------------------------------
You can build and compile this example from the root of your performance_testing_cleo directory first
by building and compiling the exectuabel for a build of your choice (serial, openmp, cuda or threads).

E.g. For a serial build of the colls0d example (see also cond0d, motion2d and thermo3d):

#. Build and compile:

   .. code-block:: console

     $ mkdir /work/bm1183/m300950/performance_testing_cleo/builds
     $ ./scripts/bash/builds.sh ./src /work/bm1183/m300950/performance_testing_cleo/builds serial openmp cuda threads
     $ ./scripts/bash/compiles.sh /work/bm1183/m300950/performance_testing_cleo/builds colls0d serial openmp cuda threads

  Note that you might want to change the team_size in the KokkosCleoSettings namespace before compilation.

#. Setup the example:

   .. code-block:: console

     $ ./scripts/collisions0d/setup_colls0d.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/CLEO \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       serial openmp cuda threads

#. (Or) If setting up cond0d:

   .. code-block:: console

     $ ./scripts/condensation0d/setup_cond0d.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/CLEO \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       serial openmp cuda threads

#. (Or) If setting up motion2d:

   .. code-block:: console

     $ ./scripts/motion2d/setup_motion2d.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/CLEO \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       serial openmp cuda threads

#. (Or) If setting up thermo3d:

   .. code-block:: console

     $ ./scripts/constthermo3d/setup_thermo3d.sh \
       /work/bm1183/m300950/bin/envs/perftests/bin/python \
       /home/m/m300950/CLEO \
       /home/m/m300950/performance_testing_cleo \
       /work/bm1183/m300950/performance_testing_cleo/builds \
       serial openmp cuda threads

#. a) Then you could perform one normal run with e.g.
``./builds/serial/collisions0d/colls0d ./builds/serial/tmp/colls0d/config_8_0.yaml``

#. b) Or e.g. run the example with the Kokkos kernel timer performance tool:

   .. code-block:: console

    $ ./scripts/bash/run_profiling.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      colls0d \
      kerneltimer.spacetimestack.memoryevents.memoryusage \
      TRUE \
      serial openmp cuda threads
    $ ./scripts/bash/postproc_profiling.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      colls0d \
      kerneltimer.spacetimestack.memoryevents.memoryusage \
      FALSE \
      serial openmp cuda threads
    $ ./scripts/bash/create_grand_datasets.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      colls0d \
      kerneltimer \
      FALSE \
      serial openmp cuda threads

#. c) You can add/remove profilers in the list of profiler names seperated by a '.',
      e.g. ``kerneltimer.spacetimestack.memoryevents.memoryusage`` to run profilers
      sequentially
