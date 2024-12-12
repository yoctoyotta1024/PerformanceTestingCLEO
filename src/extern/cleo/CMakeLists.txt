# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.29.3.zip
  GIT_TAG 3ae197ee5ff5850e9577d21eab6fe7a2bac5adb8
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.29.3 installation in: ${CLEO_BINARY_DIR}")
