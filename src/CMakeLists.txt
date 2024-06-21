# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# subdirectories for specific examples of CLEO
add_subdirectory(collisions0d EXCLUDE_FROM_ALL)
