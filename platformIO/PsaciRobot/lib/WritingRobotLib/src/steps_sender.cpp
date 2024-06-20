#include "steps_sender.h"
#include "constants.h"
#include "Arduino.h"

int stepCounterA = 0;
int stepCounterB = 0;

void set_motor_1_dir(bool dir){
  if(dir){
    PORTD &= ~(1 << DIR_PIN_MOTOR_1);  // Set DIR_PIN_MOTOR_1 HIGH
  }
  else{
    PORTD |= (1 << DIR_PIN_MOTOR_1);   // Set DIR_PIN_MOTOR_1 LOW
  }
}

void set_motor_2_dir(bool dir){
  if(dir){
    PORTD &= ~(1 << DIR_PIN_MOTOR_2);  // Set DIR_PIN_MOTOR_1 HIGH
  }
  else{
    PORTD |= (1 << DIR_PIN_MOTOR_2);   // Set DIR_PIN_MOTOR_1 LOW
  }
}

void send_steps_motor_1(int steps) {
  // Set direction
  if (steps < 0) {
    set_motor_1_dir(true);
    steps = -steps;
  }
  else set_motor_1_dir(false);

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_1();
    delay(TIME_BETWEEN_STEPS);  // Delay in milliseconds
  }
}

void send_steps_motor_2(int steps) {
  // Set direction
  if (steps < 0) {
    PORTD &= ~(1 << DIR_PIN_MOTOR_2);  // Set DIR_PIN_MOTOR_2 LOW
    steps = -steps;
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
  // Increment the internal variable
  ++stepCounterA;
  PORTD &= ~(1 << STEP_PIN_MOTOR_1);  // Set STEP_PIN_MOTOR_1 LOW
  delayMicroseconds(TIME_ON_HIGH);
  PORTD |= (1 << STEP_PIN_MOTOR_1);  // Set STEP_PIN_MOTOR_1 HIGH
}

void one_step_motor_2() {
  ++stepCounterB;
  PORTD &= ~(1 << STEP_PIN_MOTOR_2);  // Set STEP_PIN_MOTOR_2 LOW
  delayMicroseconds(TIME_ON_HIGH);
  PORTD |= (1 << STEP_PIN_MOTOR_2);  // Set STEP_PIN_MOTOR_2 HIGH
}
