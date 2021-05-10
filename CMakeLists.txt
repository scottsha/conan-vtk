cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)

if (APPLE)
	set(CMAKE_INSTALL_RPATH "@executable_path/../lib")
else()
	set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib")
endif()

set(CMAKE_BUILD_WITH_INSTALL_RPATH ON)

if(MSVC)
    # Remove pdb-related flags
    string(REGEX REPLACE "/Z[iI7]" ""
        CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
    # Embed debug info into .lib-files
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_RELEASE} /Z7")
endif()

add_subdirectory(vtk_source)
