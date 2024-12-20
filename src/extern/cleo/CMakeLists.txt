# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# fetch and make cleo library available
include(FetchContent)
FetchContent_Declare(
  cleo
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
  # URL https://github.com/yoctoyotta1024/CLEO/archive/refs/tags/v0.29.6.zip
  URL https://github.com/yoctoyotta1024/CLEO/archive/refs/heads/main.zip
  GIT_TAG cf0756c2d1f46593fea375a018f450ae15a0ec90
)
FetchContent_MakeAvailable(cleo)

message(STATUS "CLEO v0.29.6 installation in: ${CLEO_BINARY_DIR}")
