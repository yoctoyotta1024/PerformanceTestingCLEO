# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  # URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.X.Y.zip
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/heads/main.zip
  GIT_TAG e8f3706c4280ef30834aef4c089a3415d5a6d9a1
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO head of main branch, v0.X.Y, installation in: ${CLEO_BINARY_DIR}")
