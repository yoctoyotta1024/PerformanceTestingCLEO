# Changelog
All notable changes to this project will be documented in this file. See [conventional commits](https://www.conventionalcommits.org/) for commit guidelines.

- - -
## [v1.2.1](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/6ea29ce3dc8ce6d9d4da0f37d443a800b99139c1..v1.2.1) - 2024-12-09
#### Bug Fixes
- update artifacts in ci version - ([6ea29ce](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/6ea29ce3dc8ce6d9d4da0f37d443a800b99139c1)) - clara.bayley

- - -

## [v1.2.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/d4cf28e7bb9cb0354f97b15b8951b957b16f2b7a..v1.2.0) - 2024-12-09
#### Bug Fixes
- only pass numeric values to grand dataset - ([abd88de](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/abd88dea561ae094fec838bd6dbaf0215d321b24)) - clara.bayley
- open zarr dataset with correct call - ([d4cf28e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/d4cf28e7bb9cb0354f97b15b8951b957b16f2b7a)) - clara.bayley
#### Documentation
- change path2build in example - ([06b88f9](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/06b88f9d61f359fb7fb7f59ebe31a12ef74c77df)) - clara.bayley
#### Features
- option to have null profiler and set kokkos_tools_lib path explicitly - ([abbe08e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/abbe08e5c4f47a7d212a8ca0d05be1dc6da537dc)) - clara.bayley
#### Miscellaneous Chores
- add todo - ([eebf42e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/eebf42e14e1be721b1b1a23b3042093b1959e65e)) - clara.bayley
#### Refactoring
- add print statement - ([288b867](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/288b867bf1243e89fd161cbbb377faf28ff011bc)) - clara.bayley
- adapt setup for first profiling tests - ([44f804b](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/44f804bdd8ce8c3406d00d090dba2c3c1c5dcbec)) - clara.bayley
- add boolean option not to sbatch - ([82a7f08](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/82a7f08383c9d1e718f792ef323cd703ffa5b011)) - clara.bayley

- - -

## [v1.1.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/cf068be0d34056dbd8000e5364456a3d40731be2..v1.1.0) - 2024-12-09
#### Bug Fixes
- typos - ([3dab33a](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/3dab33ab9af40bd655f6323df852f62292f782d9)) - clara.bayley
- use correct yaml python package - ([61c5f8e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/61c5f8ead29125565924eab3f7307c8af512a6c1)) - clara.bayley
#### Documentation
- update how to use python scripts - ([0f2aa45](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/0f2aa45f29edaae6d9afa0acbaab67b9ec7a7a60)) - clara.bayley
- include instructions on building the performance test(s) - ([39ac1d5](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/39ac1d5a3da61f70269f5ae6eb1833638792d537)) - clara.bayley
#### Features
- new script for creating grand datasets of ensembles - ([c655917](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/c655917e86fc8831e72a276ce5d8eb38faf80fd4)) - clara.bayley
- new bash scripts to build openmp and cuda - ([720c113](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/720c113f8b585fabe784ae5b781103093b7aa77f)) - clara.bayley
- new bash scripts to build openmp and cuda - ([3275918](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/3275918516d77c6ae6ae2dd43ce2cebeef422008)) - clara.bayley
- new bash scripts to build openmp and cuda - ([f910a28](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/f910a28eea8d4e87a0486164eae8077d25a7fec9)) - clara.bayley
- new bash scripts to build openmp and cuda - ([65d9b6d](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/65d9b6df643e5eb1cc9d69f57b956238e22eaad6)) - clara.bayley
- new bash script for colls0d setup - ([c648c8b](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/c648c8b1cbd62704a229de9f6a81e35eb0997acd)) - clara.bayley
- new bash script for running postprocessing of profiling python script - ([a5cd819](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/a5cd81900f7aa0868e7b5c41c76395df563d944a)) - clara.bayley
- new bash script for running profiling python script - ([8cc895d](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/8cc895d482389dd0b303e22dedbae3b8d65efb95)) - clara.bayley
- new file for post-processing profiler outputs - ([3cd726d](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/3cd726d36fec93b53a1757e534192a5f2c45ce9a)) - clara.bayley
- new way to use profilers in run scripts - ([c0e458c](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/c0e458c21241ba35205d220a0a9fae72e27849f4)) - clara.bayley
- new bash script to help with kokkos-tools installation - ([35d8f9c](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/35d8f9ca7238500bf4b2b35e980d0a99ca80a948)) - clara.bayley
- new bash and python scripts for running executables - ([e74f03c](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/e74f03c7e43119f2ee9ce5009de8904c023f99ac)) - clara.bayley
- file rename and new file to running multiple runs - ([9e066a4](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/9e066a455105d436c0c533ca5a5dc3201eb19f85)) - clara.bayley
- scripts to generate temporary config file and input files for a setup - ([ad16d6c](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/ad16d6ccbd156307c179024af494ac454d075d7f)) - clara.bayley
- first draft of main and initial conditions scripts for long0D setup - ([df537dc](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/df537dcc866a69c53123224acb205a8ebd285744)) - clara.bayley
- add pyyaml to requirements - ([7070bf5](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/7070bf5f0bac927ee9679454418a8e7dc75b016b)) - clara.bayley
- config file for colls0D setup & main file rename - ([ba9b29e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/ba9b29e2620af1a777d8a1ed733a463a5b9ac6bb)) - clara.bayley
- scripts for main and initials conditions for 0D box collisions - ([cf068be](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/cf068be0d34056dbd8000e5364456a3d40731be2)) - clara.bayley
#### Miscellaneous Chores
- correct dates - ([dd23111](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/dd23111c9be7f651e97edcbedf9f264eebfa3418)) - clara.bayley
- file rename - ([3840cf1](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/3840cf1518b017aff49a935490aa662a92b777a6)) - clara.bayley
- file rename - ([731fc35](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/731fc353c1a53ce1b7ef562de058895e5fea5ef9)) - clara.bayley
- file rename - ([a78f312](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/a78f3125d940ba7d34f9e80a2a04516cfb5e7ae4)) - clara.bayley
- file renaming - ([f3562ae](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/f3562ae507467c5aaffee0b979b69833a12afafb)) - clara.bayley
- typos - ([b8b4ce8](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/b8b4ce88048f93e3749cdb72227f76463c114370)) - clara.bayley
#### Refactoring
- add method to write ensemble of runs to single dataset - ([18ab47d](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/18ab47df6ecaf50fac37e5c394448415eacfd06b)) - clara.bayley
- change name of zarr datasets - ([19e591e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/19e591e35e657ce0dbfe78f83022523ed0b391bb)) - clara.bayley
- generalise setup and run and postproc scripts for more than one build type - ([38b49b7](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/38b49b7e239dcef39fbcfdf53b785cd75929dbc2)) - clara.bayley
- update CLEO version - ([d616742](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/d61674215daae98386204653ee551cae2d2b82b6)) - clara.bayley
- allow conversion to zarr of space time stack profiling - ([029e08b](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/029e08be93315a8dd3b848a1894b895dbb13f521)) - clara.bayley
- move path build to later point - ([ce6fcd6](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/ce6fcd683765565023763e8dc40543ae069b7253)) - clara.bayley
- generalise python runing and postprocessing scripts - ([b3232b4](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/b3232b4badc261ff41e05c1c6f08e8beba0db8aa)) - clara.bayley
- file renameing - ([cf9e827](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/cf9e8273bc96d4439bb8005f2f6640ff315a1ed2)) - clara.bayley
- file renaming - ([3891b7a](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/3891b7a42aa4afd62174ddc6ddff4cd33c535356)) - clara.bayley
- update locations of builds and files for runs in python scripts - ([0b81d63](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/0b81d63ff4ea6de060813e8751f8c7ed7a58e24b)) - clara.bayley
- add to gitignore - ([3aed85f](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/3aed85f016b412c3a1b59ab9112fe825262e676f)) - clara.bayley
- make builds compatible with latest CLEO version - ([1da1717](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/1da17174f3da6130d636ca69f8f0df6a6c68686e)) - clara.bayley
- scripts more generic for making input files - ([72f3c5b](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/72f3c5b209400c261080d107b34a97ee9f144695)) - clara.bayley
- rename 0D -> 0d - ([fc6aaab](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/fc6aaab152fa3c3907ed29753e6024e834b9663e)) - clara.bayley
- delete pytests and fixup readme - ([9324bb0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/9324bb0153fc1b6ca9698145e1eb0798654a9306)) - clara.bayley
- use pathlib for correct paths in python - ([7af1b8b](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/7af1b8b3967833b612ac85e6325f94f706e4418d)) - clara.bayley
- change levante account - ([d626d96](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/d626d967c0073846c28b05a013b837f2097e1155)) - clara.bayley
- use latest tag for CLEO - ([fa7d100](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/fa7d10099ed812304393cec4ad7bf6740352cd6f)) - clara.bayley
- turn script into module with main function - ([88f958c](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/88f958c254b41e8be82a15536f35f85b9de9643b)) - clara.bayley
- rename executable - ([56277af](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/56277af203d8f383029d6035df6e57808c9805e4)) - clara.bayley

- - -

## [v1.0.3](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/22e0ec25e59055ead4a47748c63dfb30cd955665..v1.0.3) - 2024-09-04
#### Bug Fixes
- fix sphinx dependencies after sphinx version 8 - ([9973733](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/9973733cb6d7d56f375ca64f9d301ffcc3074865)) - clara.bayley
- Security vulnerability - ([22e0ec2](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/22e0ec25e59055ead4a47748c63dfb30cd955665)) - clara.bayley
#### Miscellaneous Chores
- formatting - ([a81363e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/a81363e626c9052dc7bf357d25c0ac897407e5e1)) - clara.bayley
#### Refactoring
- improve pre-commit - ([1035262](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/10352621c36563ad146569ab2a8b183ed91820ab)) - clara.bayley

- - -

## [v1.0.2](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/a3d50d3693c05d0469371cd223b142aad5db64e6..v1.0.2) - 2024-09-04
#### Bug Fixes
- fix sphinx dependencies after sphinx version 8 - ([a3d50d3](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/a3d50d3693c05d0469371cd223b142aad5db64e6)) - clara.bayley

- - -

## [v1.0.1](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/v0.4.0..v1.0.1) - 2024-06-21
#### Bug Fixes
- testing tags - ([52bc67e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/52bc67ea86fc4dd08e8c3417322d4494dc1cc0de)) - clara.bayley

- - -

## [v0.4.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/v0.4.0..v0.4.0) - 2024-06-21
#### Miscellaneous Chores
- **(version)** v0.4.0 - ([29e61a5](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/29e61a53039230c55f589fbd8ca4181f768bbf60)) - yoctoyotta1024

- - -

## [v0.4.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/e4cb8d544edfe0e9e9adad6186b16e97b04752ce..v0.4.0) - 2024-06-21
#### Features
- CLEO can be used as external library - ([e4cb8d5](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/e4cb8d544edfe0e9e9adad6186b16e97b04752ce)) - clara.bayley
#### Miscellaneous Chores
- **(version)** v1.0.0 - ([d4f229b](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/d4f229bbcf861e0033da48ff0590ed3161048dd6)) - clara.bayley

- - -

## [v1.0.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/e4cb8d544edfe0e9e9adad6186b16e97b04752ce..v1.0.0) - 2024-06-21
#### Features
- CLEO can be used as external library - ([e4cb8d5](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/e4cb8d544edfe0e9e9adad6186b16e97b04752ce)) - clara.bayley

- - -

## [v0.3.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/36dba4ad1ae0175447caa6f1ecc4b8b36b433270..v0.3.0) - 2024-06-21
#### Bug Fixes
- make kokkos and cleo includes work - ([829e4e3](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/829e4e3055e6500a812d0dac8d4e930098c97903)) - clara.bayley
- correct conda environment - ([06029a3](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/06029a3955290835a799372fe23e07f0eaa72eeb)) - clara.bayley
- correct urls in changelog - ([83a7c80](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/83a7c806396c4de3dc963fcbf9f986fedbefee9b)) - clara.bayley
- use correct repo for cog - ([4b37a66](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/4b37a6683168767a3c8879965bea82378189e517)) - clara.bayley
#### Features
- importing CLEO library, building and compiling works - ([6b4295e](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/6b4295e5c5680730286b289d72c5afdd0f7ca904)) - clara.bayley
- CMakeLists used to fetch external libraries for CLEO, Kokkos and yaml-cpp - ([36dba4a](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/36dba4ad1ae0175447caa6f1ecc4b8b36b433270)) - clara.bayley
#### Miscellaneous Chores
- formatting - ([a152cd8](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/a152cd895bfc577db295ef7d68adb249d1e44695)) - clara.bayley

- - -

## [v0.2.0](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/compare/5f19b9318f501442018bc321f27f02825b14ab02..v0.2.0) - 2024-06-21
#### Features
- more pre-commit and CI features - ([b0f7cc5](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/b0f7cc5c53e4098e7d77038cfb3b48711cf65ab6)) - clara.bayley
- add cog config file - ([5f19b93](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/5f19b9318f501442018bc321f27f02825b14ab02)) - clara.bayley
#### Miscellaneous Chores
- formatting - ([a0dcc24](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/a0dcc24adaac522fe1c779f45c4477e549f7c0f6)) - clara.bayley
#### Refactoring
- delete unwanted header - ([f9f0673](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/f9f06738da40495f820ee28f6961aa661aa3b28d)) - clara.bayley
- update version - ([2fa40c4](https://github.com/yoctoyotta1024/PerformanceTestingCLEO/commit/2fa40c46ee195d774c1265ad125dcc44d993a359)) - clara.bayley

- - -

Changelog generated by [cocogitto](https://github.com/cocogitto/cocogitto).
