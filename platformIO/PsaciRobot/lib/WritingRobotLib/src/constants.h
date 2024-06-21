#ifndef CONSTANTS_H
#define CONSTANTS_H

#define MOTOR_SPEED_A 2000
#define MOTOR_SPEED_B 2000

// Constants
#define TIME_BETWEEN_STEPS 1  // Time between steps in milliseconds
#define TIME_ON_HIGH 100      // Time duration for step pin high in microseconds
#define TIME_AFTER_STEPS 5    // Delay after steps in milliseconds
#define STEP_ANGLE 0.9        // Angle per step
#define MICRO_STEP 16         // How much steps for one step

/*
----------------------------------------------------------
    WARNING - STEP PINS HAVE TO BE LESS THAN 8
    USAGE OF THE DIRECT REGISTER MANIPULATIONS
    OTHERWISE THE STEP FUNCTION NEEDS THE MODIFICATIONS
----------------------------------------------------------
*/

// Pins MOTOR 1
#define DIR_PIN_MOTOR_1 5       // Pin number for DIR_PIR of motor1
#define STEP_PIN_MOTOR_1 6      // Pin number for STEP_PIR of motor1

// Pins MOTOR 2
#define DIR_PIN_MOTOR_2 3           // Pin number for DIR_PIR of motor2
#define STEP_PIN_MOTOR_2 4          // Pin number for STEP_PIR of motor2

// MCP2515 settings
#define MPC_CS_PIN 10               // Chip select pin for MCP2515
#define MPC_BITRATE CAN_125KBPS     // 
#define MPC_CLOCK MCP_8MHZ          //

#endif
