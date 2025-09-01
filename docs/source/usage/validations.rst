.. _validations:

Running Validations
===================

Having cloned the repository, start by building, compiling and running a test
in a build directory of your choice, as you would for a performance test.

Example: Condensation0d Validation in Serial
--------------------------------------------
You can build and compile this example from the root of your performance_testing_cleo directory.
See :ref:`running the performance tests<perftests>` for more instructions.

_Note:_ Before compiling the example you may need to activate data output for the test case
by changing the Observer returned by the ```inline Observer auto create_observer``` function in
your executables ``main_[xxx].cpp`` file. E.g. uncomment the lines leading to
``return obssd >> obs1 >> obs0;`` and comment out the line ``return NullObserver{};``

#. Then you could perform one normal run with e.g.
  ``./builds/serial/condensation0d/cond0d ./builds/serial/tmp/cond0d/config_1_128_1_0.yaml``
  (it is recomended that you create the output directory before running the model). Or
  you can run the example with Kokkos performance tool(s), e.g.

   .. code-block:: console

    $ ./scripts/bash/run_profiling.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      cond0d \
      kerneltimer.spacetimestack.memoryevents.memoryusage \
      TRUE \
      serial openmp cuda threads

#. Finally plot the results with the validation script, e.g.

   .. code-block:: console

    $ ./scripts/bash/validation.sh \
      /work/bm1183/m300950/bin/envs/perftests/bin/python \
      /home/m/m300950/CLEO \
      /home/m/m300950/performance_testing_cleo \
      /work/bm1183/m300950/performance_testing_cleo/builds \
      cond0d \
      1 128 1 0 \
      sol.zarr setup.txt \
      serial openmp cuda threads
