# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/heads/performance_testing_cleo.zip
  GIT_TAG c505dfbe747360ed5de8485421be338db3c3e398
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO head of performance_testing_cleo branch, variant of v0.39.0, installation in: ${CLEO_BINARY_DIR}")
