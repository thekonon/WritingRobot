#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

void moveStraight(int stepsA, int stepsB, int speedA, int speedB);
void moveArc(int stepsA, int stepsB, int speedA, int speedB);

extern int stepCounterA;
extern int stepCounterB;

#endif // MOTOR_CONTROL_H
