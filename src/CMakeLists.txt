# set cmake version
cmake_minimum_required(VERSION 3.18.0)

project(project
  LANGUAGES CXX
  DESCRIPTION "PerformanceTestingCLEO by Clara Bayley"
  VERSION 2.8.0
)

message("CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
message("CMAKE_BINARY_DIR: ${CMAKE_BINARY_DIR}")

# ensure C++ compiler uses certain settings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
set(CMAKE_CXX_STANDARD "20")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CXX_EXTENSIONS ON)

# install CLEO for project
set(cleopath ${CMAKE_SOURCE_DIR}/extern/cleo)
message(STATUS "Using CLEO installation from: ${cleopath}")
add_subdirectory(${cleopath})

message("CLEO_SOURCE_DIR: ${CLEO_SOURCE_DIR}")
message("CLEO_BINARY_DIR: ${CLEO_BINARY_DIR}")

# print default compiler flags
message(STATUS "CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")

# add directories of from src
add_subdirectory(collisions0d EXCLUDE_FROM_ALL)
add_subdirectory(condensation0d EXCLUDE_FROM_ALL)
add_subdirectory(motion2d EXCLUDE_FROM_ALL)
add_subdirectory(constthermo3d EXCLUDE_FROM_ALL)
