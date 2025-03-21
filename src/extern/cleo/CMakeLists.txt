# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.38.0.zip
  GIT_TAG 1cef224c092f220e5560dcc041922ba05160f523
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO head of main branch, v0.38.0, installation in: ${CLEO_BINARY_DIR}")
