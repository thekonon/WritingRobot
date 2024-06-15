#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

void moveStraight(int stepsA, int stepsB, int speedA, int speedB);
void moveArc(int stepsA, int stepsB, int speedA, int speedB);
int calculate_required_steps(float wanted_angle, int current_step);
void send_steps_motor_1(int steps);
void send_steps_motor_2(int steps);
void one_step_motor_1();
void one_step_motor_2();


extern int stepCounterA;
extern int stepCounterB;

#endif // MOTOR_CONTROL_H
