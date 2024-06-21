# set cmake version
cmake_minimum_required(VERSION 3.18.0)

project(project
  LANGUAGES CXX
  DESCRIPTION "PerformanceTestingCLEO by Clara Bayley"
  VERSION 0.1.0
)

# ensure C++ compiler uses certain settings
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
set(CMAKE_CXX_STANDARD "20")
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CXX_EXTENSIONS ON)

# install CLEO for project
set(cleopath ${CMAKE_SOURCE_DIR}/extern/cleo)
message(STATUS "Using CLEO installation from: ${cleopath}")
add_subdirectory(${cleopath})

# install Kokkos for project
set(kokkospath ${CMAKE_SOURCE_DIR}/extern/kokkos)
message(STATUS "Using Kokkos installation from: ${kokkospath}")
add_subdirectory(${kokkospath})

# install yaml-cpp for project
set(yamlcpppath ${CMAKE_SOURCE_DIR}/extern/yaml-cpp)
message(STATUS "Using yaml-cpp installation from: ${yamlcpppath}")
add_subdirectory(${yamlcpppath})

# print default compiler flags
message(STATUS "CMAKE_CXX_FLAGS: ${CMAKE_CXX_FLAGS}")

# add directories of from src
add_subdirectory(src)
