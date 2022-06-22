#project(test_vtk_conan_package)
#cmake_minimum_required(VERSION 3.16)
#
#set(CMAKE_CXX_STANDARD 20)
#
#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()
#
#if(APPLE)
#    # Workaround for rpath error
#    set(CMAKE_SKIP_RPATH 0)
#endif(APPLE)
#
##------------------------------#
##    FIND COMMON CONAN LIBS
##------------------------------#
#find_package(vtk REQUIRED)
#
##------------------------------#
##    SUBPROJECTS
##------------------------------#
#include_directories(src)
#add_subdirectory(src)
#add_subdirectory(apps)
#add_subdirectory(pyphysnometry_src)
#add_subdirectory(unit_tests)
#
#
#file(GLOB SOURCE_FILES *.cpp)
#
#add_executable(${PROJECT_NAME} ${SOURCE_FILES})
#target_link_libraries(${PROJECT_NAME} PUBLIC
#        vtk::vtk)

cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_CXX_STANDARD 20)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

if(APPLE)
    # Workaround for rpath error
    set(CMAKE_SKIP_RPATH 0)
endif(APPLE)

add_executable(${PROJECT_NAME} test_package.cpp )

target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} ${CMAKE_DL_LIBS})

if(UNIX AND NOT APPLE)
    TARGET_LINK_LIBRARIES(${PROJECT_NAME} m)
endif()

