# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.33.0.zip
  GIT_TAG 641349a806ea5dca070192ba997b08387863eb88
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.33.0 installation in: ${CLEO_BINARY_DIR}")
