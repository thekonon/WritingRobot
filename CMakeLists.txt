cmake_minimum_required(VERSION 3.10)
project(MotorControlTests)  # Project name

# Specify the C++ standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_BINARY_DIR ${PROJECT_SOURCE_DIR}/platformIO/PsaciRobot/build)


# Include directories
include_directories(${PROJECT_SOURCE_DIR}/platformIO/PsaciRobot/lib/WritingRobotLib/src)
include_directories(${PROJECT_SOURCE_DIR}/platformIO/PsaciRobot/test/test_steps_sender)
include_directories(${PROJECT_SOURCE_DIR}/unity/src)

# Source files
set(SRC_FILES
    platformIO/PsaciRobot/lib/WritingRobotLib/src/motor_control.cpp
    platformIO/PsaciRobot/lib/WritingRobotLib/src/steps_sender.cpp
    platformIO/PsaciRobot/test/test_steps_sender/MockArduino.cpp
)

set(TEST_STEPS_SENDER_FILES
    platformIO/PsaciRobot/test/test_steps_sender/test_steps_sender.cpp
    unity/src/unity.c
)

# Add the executable
add_executable(test_steps_sender ${SRC_FILES} ${TEST_STEPS_SENDER_FILES})
set_property(TARGET test_steps_sender PROPERTY COMPILE_DEFINITIONS UNIT_TEST)
