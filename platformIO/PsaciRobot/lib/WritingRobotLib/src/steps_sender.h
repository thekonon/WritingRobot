#ifndef STEPS_SENDER_H
#define STEPS_SENDER_H

void set_motor_1_dir(bool dir);
void set_motor_2_dir(bool dir);
void send_steps_motor_1(int steps);
void send_steps_motor_2(int steps);
void one_step_motor_1(bool dir);
void one_step_motor_2(bool dir);

// State variables to track the current motor rotation
extern int stepCounterA;
extern int stepCounterB;

#endif // STEPS_SENDER_H