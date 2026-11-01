cmake_minimum_required(VERSION 3.15)

project(newton_solve VERSION 1.0.0 LANGUAGES CXX)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

add_executable(main src/main.cpp)

target_compile_features(main PRIVATE cxx_std_17)
set_target_properties(main PROPERTIES
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF)

if (MSVC)
    target_compile_options(main PRIVATE /utf-8 /W4 /permissive-)
else()
    target_compile_options(main PRIVATE -Wall -Wextra -Wpedantic)
endif()

set_target_properties(main PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY                 "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG           "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE         "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO  "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL      "${CMAKE_BINARY_DIR}")
