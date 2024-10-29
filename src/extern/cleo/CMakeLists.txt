# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/releases/tag/v0.27.0
  GIT_REPOSITORY https://github.com/yoctoyotta1024/CLEO
  GIT_TAG v0.27.0
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.27.0 installation in: ${CLEO_BINARY_DIR}")
