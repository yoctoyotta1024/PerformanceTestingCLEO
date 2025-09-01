.. PerformanceTestingCLEO documentation master file, based off sphinx-quickstart.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PerformanceTestingCLEO's Documentation!
==================================================

This repository has been made to document the performance tests of CLEO on Levante for CLEO's
first model description paper. Specifically it tests the branch ``performance_testing_cleo``, which
is the same as CLEO ``v0.39.0`` with the patch
``0001-refactor-comment-out-checking-initialisation-for-gbx.patch`` applied.

To (locally) reproduce this project, simply clone this repository and ``CLEO`` and checkout ``CLEO``
to the ``performance_testing_cleo`` branch (or apply the patch). You will need to setup an
environment with the dependencies installed and then run ``pre-commit install``, but other than
that everything should work out of the box and you can now run & have fun with the project...
If not, please raise an issue on the GitHub repository.

Time to get involved! Check out the :doc:`getting started page<usage/getstart>`.

Contents
--------
.. toctree::
   :maxdepth: 1

   usage/getstart
   usage/perftests
   usage/validations
   usage/ourdocs

   GitHub Repo <https://github.com/yoctoyotta1024/PerformanceTestingCLEO.git>
   usage/contributing
   usage/contact
   references

Questions?
----------
Yes please! Simply :ref:`contact us! <contact>`

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
