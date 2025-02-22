cmake_minimum_required(VERSION 3.10)
project(TCurve)  # Project name

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)  # or 17, depending on your needs
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# # Include Unity test
include_directories(${PROJECT_SOURCE_DIR}/src/TCurve)
include_directories(${PROJECT_SOURCE_DIR}/unity/src)

# Source files
set(SRC_FILES
    src/TCurve/TCurve.cpp
)

set(TEST_SRC_FILES
    test/test_SCurve.cpp
    unity/src/unity.c
)

# add_executable(build_tcurve_lib ${SRC_FILES})

# # Add the executable
add_executable(test_tcurve_lib ${SRC_FILES} ${TEST_SRC_FILES})
set_property(TARGET test_tcurve_lib PROPERTY COMPILE_DEFINITIONS UNIT_TEST)
# # 