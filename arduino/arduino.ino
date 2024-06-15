#include <SPI.h>
#include <mcp2515.h>
#include <math.h>
#include <constants.h>

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
float read_and_filter();
int calculate_required_steps(float filtered_value, int *current_step);
void send_steps_motor_1(int steps);
void send_steps_motor_2(int steps);
void one_step_motor_1();
void one_step_motor_2();
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
    // Serial.print("CAN MSG found, id: ");
    // Serial.print(canMsg1.can_id, HEX);
    // Serial.print(" DLC: ");
    // Serial.print(canMsg1.can_dlc, HEX);
    // Serial.print(" Data: ");
    // for (int i = 0; i < canMsg1.can_dlc; i++) {
    //   Serial.print(canMsg1.data[i], HEX);
    //   Serial.print(" | ");
    // }
    // Serial.println();

    // Get required position from CAN
    motor_1_angle_wanted = canMsg1.data[0] * 255 + canMsg1.data[1];// + float(canMsg1.data[2] * 255 + canMsg1.data[3]) / 10000;
    motor_2_angle_wanted = canMsg1.data[4] * 255 + canMsg1.data[5];// + float(canMsg1.data[6] * 255 + canMsg1.data[7]) / 10000;

    // Serial.print("Value wanted: ");
    // Serial.print(motor_1_angle_wanted);

    // Serial.print(" Current value: ");
    // Serial.print(motor_1_current_angle);

    // Calculate required steps
    steps_needed_motor_1 = calculate_required_steps(motor_1_angle_wanted, &motor_1_current_angle);
    steps_needed_motor_2 = calculate_required_steps(motor_2_angle_wanted, &motor_2_current_angle);

    send_steps_motor_1(steps_needed_motor_1);
    send_steps_motor_2(steps_needed_motor_2);
    delay(TIME_AFTER_STEPS);  // Delay in milliseconds
  }
  //Serial.println("Sending 10 steps");

  //delay(250);
}

void set_position_motor_1(float position){
    steps_needed_motor_1 = calculate_required_steps(position, &current_step_motor_1);
    printf("Needed steps: %d\n", steps_needed_motor_1);
    send_steps_motor_1(steps_needed_motor_1);
}

int calculate_required_steps(float wanted_angle, float *current_angle) {
  // Calculate the difference in angle
  float diff = *current_angle - wanted_angle;

  // Normalize the difference to be within the range [-180, 180)
  if (diff > 180) {
    diff -= 360;
  } else if (diff < -180) {
    diff += 360;
  }

  // Calculate steps needed
  int steps_needed = (int)(diff / STEP_ANGLE * MICRO_STEP);

  // Update the current angle
  float res = steps_needed * STEP_ANGLE / MICRO_STEP;
  *current_angle = fmod(*current_angle - res, 360);
  if (*current_angle < 0) {
    *current_angle += 360;
  }

  return steps_needed;  // Return the calculated steps
}

void send_steps_motor_1(int steps) {
  // Set direction
  if (steps < 0) {
    steps = abs(steps);
    Serial.println("Setting the dir pin of motor 1 to HIGH");
    digitalWrite(DIR_PIN_MOTOR_1, HIGH);  // Set DIR_PIN_MOTOR_1 LOW
  } else {
    Serial.println("Setting the dir pin of motor 1 to LOW");
    digitalWrite(DIR_PIN_MOTOR_1, LOW);  // Set DIR_PIN_MOTOR_1 HIGH
  }

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_1();
    delay(TIME_BETWEEN_STEPS);  // Delay in milliseconds
  }
}

void send_steps_motor_2(int steps) {
  // Set direction
  if (steps < 0) {
    steps = abs(steps);
    PORTD &= ~(1 << DIR_PIN_MOTOR_2);  // Set DIR_PIN_MOTOR_2 LOW
  } else {
    PORTD |= (1 << DIR_PIN_MOTOR_2);  // Set DIR_PIN_MOTOR_2 HIGH
  }

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_2();
    delay(TIME_BETWEEN_STEPS);  // Delay in milliseconds
  }
}

void one_step_motor_1() {
  PORTD &= ~(1 << STEP_PIN_MOTOR_1);  // Set STEP_PIN_MOTOR_1 LOW
  delayMicroseconds(TIME_ON_HIGH);
  PORTD |= (1 << STEP_PIN_MOTOR_1);  // Set STEP_PIN_MOTOR_1 HIGH
}

void one_step_motor_2() {
  PORTD &= ~(1 << STEP_PIN_MOTOR_2);  // Set STEP_PIN_MOTOR_2 LOW
  delayMicroseconds(TIME_ON_HIGH);
  PORTD |= (1 << STEP_PIN_MOTOR_2);  // Set STEP_PIN_MOTOR_2 HIGH
}
