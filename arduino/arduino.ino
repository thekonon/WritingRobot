#include <SPI.h>
#include <mcp2515.h>
#include <math.h>
#include "src/constants.h"
#include "src/motor_control.h"
#include "src/steps_sender.h"

// Variables
struct can_frame canMsg1;
MCP2515 mcp2515(10);

float motor_1_angle_wanted = 0.0;
float motor_2_angle_wanted = 0.0;
float motor_1_current_angle = 130.0;
float motor_2_current_angle = 200.0;
float diff;
int current_step_motor_1 = 0;
int steps_needed_motor_1 = 0;
int current_step_motor_2 = 0;
int steps_needed_motor_2 = 0;

// Function prototypes
void set_position_motor_1(float angle);
void set_position_motor_2(float angle);

void setup() {
  Serial.begin(115200);

  // Set up CAN communication
  Serial.println("CAN BUS communication initialization");
  mcp2515.reset();
  mcp2515.setBitrate(CAN_125KBPS, MCP_8MHZ);
  mcp2515.setNormalMode();
  Serial.println("CAN BUS communication initialized");

  // Set up output pins for motor 1
  pinMode(STEP_PIN_MOTOR_1, OUTPUT);
  pinMode(DIR_PIN_MOTOR_1, OUTPUT);

  // Set up output pins for motor 2
  pinMode(STEP_PIN_MOTOR_2, OUTPUT);
  pinMode(DIR_PIN_MOTOR_2, OUTPUT);

  digitalWrite(STEP_PIN_MOTOR_1, HIGH);
  digitalWrite(STEP_PIN_MOTOR_2, HIGH);
}

void loop() {
  if (mcp2515.readMessage(&canMsg1) == MCP2515::ERROR_OK) {

    // Get required position from CAN
    motor_1_angle_wanted = canMsg1.data[0] * 255 + canMsg1.data[1];// + float(canMsg1.data[2] * 255 + canMsg1.data[3]) / 10000;
    motor_2_angle_wanted = canMsg1.data[4] * 255 + canMsg1.data[5];// + float(canMsg1.data[6] * 255 + canMsg1.data[7]) / 10000;

    // Calculate required steps
    steps_needed_motor_1 = calculate_required_steps(motor_1_angle_wanted, current_step_motor_1);
    steps_needed_motor_2 = calculate_required_steps(motor_2_angle_wanted, current_step_motor_2);

    send_steps_motor_1(steps_needed_motor_1);
    send_steps_motor_2(steps_needed_motor_2);
    delay(TIME_AFTER_STEPS);  // Delay in milliseconds
  }
  //Serial.println("Sending 10 steps");

  //delay(250);
}