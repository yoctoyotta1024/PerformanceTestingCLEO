# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.19.0.tar.gz
  GIT_TAG b8c6b2624a83b35bd9a9bf9680725d0c56dd72dd
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.19.0 installation in: ${CMAKE_BINARY_DIR}/_deps/cleo")
