# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.30.1.zip
  GIT_TAG e0b7be787984ad71b89bf7fe7c0c71df6d0dbdde
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.30.1 installation in: ${CLEO_BINARY_DIR}")
