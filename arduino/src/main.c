#include <stdio.h>
#include <math.h>
#include <constants.h>

const int MAGIC_CONSTANT = 10; // constant for splitting the line

// Testing steps
int current_motor_step_1 = 0;
int current_motor_step_2 = 0;
int current_motor_dir_1 = 1;
int current_motor_dir_2 = 1;


float motor_1_value = 0.0;
float motor_2_value = 0.0;
float current_angle = 0.0;
float diff = 0.0;
int current_step_motor_1 = 0;
int steps_needed_motor_1 = 0;
int current_step_motor_2 = 0;
int steps_needed_motor_2 = 0;

// // Function prototypes
// float read_and_filter();
// int calculate_required_steps(float filtered_value, int current_step);
// void send_steps_motor_1(int steps);
// void send_steps_motor_2(int steps);
// void one_step_motor_1();
// void one_step_motor_2();
// void set_motors_position(float motor_1, float motor_2);

int main(){
    // printf("Current motor_1 position: %d\n", current_motor_step_1);
    set_motors_position(1, 1);
    printf("Current motor_1 position: %d\n", current_motor_step_1);
    set_motors_position(0, 0);
    printf("Current motor_1 position: %d\n", current_motor_step_1);
    printf("Current motor_2 position: %d\n", current_motor_step_2);
    return 0;
}

void set_motors_position(float motor_1, float motor_2){
    steps_needed_motor_1 = calculate_required_steps(motor_1, &current_step_motor_1);
    steps_needed_motor_2 = calculate_required_steps(motor_2, &current_step_motor_2);
    // printf("Needed steps for motor 1: %d\n", steps_needed_motor_1);
    // printf("Needed steps for motor 2: %d\n", steps_needed_motor_2);
    int division = (int)ceil((float)sqrt(steps_needed_motor_1*steps_needed_motor_1 + steps_needed_motor_2*steps_needed_motor_2) * MAGIC_CONSTANT);
    float multiplier_1 = (float)steps_needed_motor_1 / division;
    float multiplier_2 = (float)steps_needed_motor_2 / division;
    
    float progress1 = 0;
    float progress2 = 0;
    int res_1, res_2;
    float percentage;
    int sum = 0;
    int i = 1;
    for (i = 1; i <= division; i++) {
        res_1 = round(multiplier_1 * i - progress1);
        if (res_1 != 0) {
            progress1 += res_1;
            percentage = (progress1 / steps_needed_motor_1) * 100;
            // printf("MOTOR1: %.2f%%\n", percentage);
            send_steps_motor_1(res_1);
        }
        res_2 = round(multiplier_2 * i - progress2);
        if (res_2 != 0) {
            progress2 += res_2;
            percentage = (progress2 / steps_needed_motor_2) * 100;
            // printf("MOTOR2: %.2f%%\n", percentage);
            send_steps_motor_2(res_2);
        }
    }
}

int calculate_required_steps(float wanted_angle, int current_step) {
    float current_angle = current_step * STEP_ANGLE / MICRO_STEP;
    float diff_angle = wanted_angle - current_angle;
    return (int)round(diff_angle*MICRO_STEP/STEP_ANGLE);
}

void send_steps_motor_1(int steps) {
  // Set direction
  if (steps < 0) {
    steps = abs(steps);
    current_motor_dir_1 = -1;
    // printf("Setting direction to negative\n");
  }else{
    current_motor_dir_1 = 1;
    // printf("Setting direction to positive\n");
  }

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_1();
  }
}

void send_steps_motor_2(int steps) {
  // Set direction
  if (steps < 0) {
    steps = abs(steps);
    current_motor_dir_2 = -1;
  }else{
    current_motor_dir_2 = 1;
  }

  // Send steps
  for (int i = 0; i < steps; i++) {
    one_step_motor_2();
  }
}

void one_step_motor_1() {
  // printf("Sending 1 step\n");
  current_motor_step_1 += current_motor_dir_1;
}

void one_step_motor_2() {
  current_motor_step_2 += current_motor_dir_2;
    //printf("MOTOR2: Sending 1 step\n");
}