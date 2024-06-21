.. _getstart:

Getting Started
===============

Clone PerformanceTestingCLEO's GitHub repository:

.. code-block:: console

  $ git clone https://github.com/yoctoyotta1024/PerformanceTestingCLEO.git

and then create an environment with the necessary dependencies installed (using micromamba, mamba
or conda as listed in the environment.yml):

.. code-block:: console

  $ conda env create --file environment.yml --prefix [name for your environment]
  $ conda activate [name of your environment]

Finally install the pre-commit hooks:

.. code-block:: console

  $ pre-commit install

which will be used when you try to commit something or you execute ``pre-commit run``. You can learn
more about the powers of pre-commit from `their documentation <https://pre-commit.com>`_.

That's it, you're done!
