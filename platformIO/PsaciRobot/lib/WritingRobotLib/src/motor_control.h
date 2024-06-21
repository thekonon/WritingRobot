#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

void moveStraight(int stepsA, int stepsB, int speedA, int speedB);
void moveArc(int stepsA, int stepsB, int speedA, int speedB);
int calculate_required_steps(float wanted_angle, int current_step);


#endif // MOTOR_CONTROL_H
