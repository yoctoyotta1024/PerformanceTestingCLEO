# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.37.0.zip
  GIT_TAG bcfd94269ebb944ad381e4aa8495ecad05b8760f
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO head of main branch, v0.37.0, installation in: ${CLEO_BINARY_DIR}")
