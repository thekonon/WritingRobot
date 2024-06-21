#include "steps_sender.h"

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
  int dir = true;
  // Set direction
  if (steps < 0) 
  {
    set_motor_1_dir(true);
    dir = false;
    steps = -steps;
  }else
  {
    set_motor_1_dir(false);
  }

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_1(dir);
    delay(TIME_BETWEEN_STEPS);  // Delay in milliseconds
  }
}

void send_steps_motor_2(int steps) {
  bool dir = true;
  // Set direction
  if (steps < 0) {
    dir = false;
    set_motor_2_dir(true);
    steps = -steps;
  } else {
    set_motor_2_dir(false);
  }

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_2(dir);
    delay(TIME_BETWEEN_STEPS);  // Delay in milliseconds
  }
}

void one_step_motor_1(bool dir) {
  if (dir) ++stepCounterA; else --stepCounterB;
  PORTD &= ~(1 << STEP_PIN_MOTOR_1);  // Set STEP_PIN_MOTOR_1 LOW
  delayMicroseconds(TIME_ON_HIGH);
  PORTD |= (1 << STEP_PIN_MOTOR_1);  // Set STEP_PIN_MOTOR_1 HIGH
}

void one_step_motor_2(bool dir) {
  if (dir) ++stepCounterA; else --stepCounterB;
  PORTD &= ~(1 << STEP_PIN_MOTOR_2);  // Set STEP_PIN_MOTOR_2 LOW
  delayMicroseconds(TIME_ON_HIGH);
  PORTD |= (1 << STEP_PIN_MOTOR_2);  // Set STEP_PIN_MOTOR_2 HIGH
}
