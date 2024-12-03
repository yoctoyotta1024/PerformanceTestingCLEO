# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  # GIT_REPOSITORY https://github.com/yoctoyotta1024/CLEO
  # GIT_TAG v0.28.4
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.28.4.zip
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.28.4 installation in: ${CLEO_BINARY_DIR}")
