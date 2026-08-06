cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_BUILD_TYPE Debug)
project(TCurveProject)

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/inc)
include_directories(${PROJECT_SOURCE_DIR}/src)

# Source files
set(SRC_FILES ${PROJECT_SOURCE_DIR}/src/tcurve.cpp)

# Create a static library for TCurve
add_library(TCurve SHARED  ${SRC_FILES})
target_compile_definitions(TCurve
    PRIVATE TCURVE_EXPORTS
)
# Main application
set(TCURVE_APP_SRC ${PROJECT_SOURCE_DIR}/main.cpp)
add_executable(TCurveApp ${TCURVE_APP_SRC})
target_link_libraries(TCurveApp PRIVATE TCurve)  # Ensure linking with TCurve

# Enable testing
add_subdirectory(analysis)
enable_testing()
add_subdirectory(test)
