#include "steps_sender.h"
#include "constants.h"
#include "Arduino.h"

void send_steps_motor_1(int steps) {
  // Set direction
  if (steps < 0) {
    steps = abs(steps);
    digitalWrite(DIR_PIN_MOTOR_1, 1);  // Set DIR_PIN_MOTOR_1 LOW
  } else {
    digitalWrite(DIR_PIN_MOTOR_1, 0);  // Set DIR_PIN_MOTOR_1 HIGH
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
