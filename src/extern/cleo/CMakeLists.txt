# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.33.1.zip
  GIT_TAG c2734f24b9b39163c15f1c67cc1582aac9b376fa
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.33.1 installation in: ${CLEO_BINARY_DIR}")
