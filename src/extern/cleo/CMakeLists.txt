# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.38.2.zip
  GIT_TAG 69b35bcff32a17a5c3fcccf1b7c2cc53df8d8c5d
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO head of main branch, v0.38.2, installation in: ${CLEO_BINARY_DIR}")
