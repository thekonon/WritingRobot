cmake_minimum_required(VERSION 3.10)
project(MotorControlTests)

# Specify the C standard
set(CMAKE_C_STANDARD 23)

# Include directories
include_directories(${PROJECT_SOURCE_DIR}/arduino/src)
include_directories(${PROJECT_SOURCE_DIR}/arduino/unity/src)


# include_directories("C:\\Users\\theko\\AppData\\Local\\Arduino15\\packages\\arduino\\tools\\avr-gcc\\7.3.0-atmel3.6.1-arduino7\\avr\\include")
# include_directories("C:\\Users\\theko\\AppData\\Local\\Arduino15\\packages\\arduino\\hardware\\avr\\1.8.6\\cores\\arduino")
# include_directories("C:\\Users\\theko\\AppData\\Local\\Arduino15\\packages\\arduino\\hardware\\avr\\1.8.6\\variants")


# Source files
set(SRC_FILES
    arduino/src/motor_control.cpp
)

set(TEST_FILES
    arduino/test/test_motor_control.c
    arduino/unity/src/unity.c
)

# Add the executable
add_executable(test_runner ${SRC_FILES} ${TEST_FILES})

# Add the executable for main program
# add_executable(main_program ${SRC_FILES})
