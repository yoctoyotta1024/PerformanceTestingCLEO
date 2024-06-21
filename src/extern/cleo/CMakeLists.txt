# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  # URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.20.0.tar.gz # TODO(CB): use new tag
  GIT_REPOSITORY https://github.com/yoctoyotta1024/CLEO
  GIT_TAG 6e092c6475db4364703c05d82843cc96d2e10f3f
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.20.0 installation in: ${CLEO_BINARY_DIR}")
