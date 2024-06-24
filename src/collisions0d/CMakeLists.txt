# set cmake version
if(NOT DEFINED CMAKE_MINIMUM_REQUIRED_VERSION)
  cmake_minimum_required(VERSION 3.18.0)
endif()

# set project name and print directory of this CMakeLists.txt (source directory of project)
project("collisions0d")
message("PROJECT_SOURCE_DIR: ${PROJECT_SOURCE_DIR}")

# Set libraries from CLEO to link with executable
set(CLEOLIBS gridboxes initialise observers runcleo superdrops zarr)

# create primary executable
set(exec colls0D)
add_executable(${exec} EXCLUDE_FROM_ALL "main.cpp")

# Add directories and link libraries to target
target_link_libraries(${exec} PRIVATE cartesiandomain "${CLEOLIBS}")
target_link_libraries(${exec} PUBLIC Kokkos::kokkos)
target_include_directories(${exec} PRIVATE "${CLEO_SOURCE_DIR}/libs") # CLEO libs directory

# set specific C++ compiler options for target (optional)
#target_compile_options(${exec} PRIVATE)

# set compiler properties for target(s)
set_target_properties(${exec} PROPERTIES
  CMAKE_CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS ON
  CXX_STANDARD 20)
