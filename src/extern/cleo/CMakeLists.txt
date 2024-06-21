# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.20.0.tar.gz
  GIT_TAG c678866aacc9b749179fda4b86a1dfc357a28c7a
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.20.0 installation in: ${CMAKE_BINARY_DIR}/_deps/cleo")
