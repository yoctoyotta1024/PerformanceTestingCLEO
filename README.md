# Performance Testing of CLEO On Levante for First Model Description Paper

This repository has been made to document the performance tests of CLEO on Levante for CLEO's
first model description paper.

## Install
To (locally) reproduce this project simply clone the repository:
```
git clone https://github.com/yoctoyotta1024/PerformanceTestingCLEO.git
```
and then create an environment with the necessary dependencies installed (using micromamba, mamba
or conda as listed in the environment.yml):
```
conda env create -f environment.yml --prefix [name for your environment]
conda activate [name of your environment]
```
Finally you need to run ``pre-commit install`` but other than that everything should work out of
the box and you can now have fun with the project... If not, please raise an issue on the
GitHub repository.

## Documentation
Some documentation has been set up for this project which you should be able to find hosted online
here:
### https://yoctoyotta1024.github.io/PerformanceTestingCLEO/
... If not, please raise an issue on the GitHub repository.

Alternatively, You can build and view the documentation locally. First build the .xml
files using Doxygen followed by .html files using Sphinx, then view the .html in your default
browser. E.g.

```
cd ./docs && mkdir build && mkdir build/doxygen
doxygen doxygen/doxygen.dox && make html
open build/html/index.html
```

Thank you and good luck!

## Contributors
- Clara Bayley
