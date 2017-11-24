PROJECT(testpkg)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

find_package("OpenAL")

IF(OPENAL_FOUND)
    ADD_EXECUTABLE(testpkg testpkg.c)
    include_directories(${OPENAL_INCLUDE_DIR})
    TARGET_LINK_LIBRARIES(testpkg ${OPENAL_LIBRARY})
ELSE()
    MESSAGE(FATAL_ERROR "OpenAL not found")
ENDIF()
