#include "motor_control.h"
#include "constants.h"
#include "math.h"

int stepCounterA = 0;
int stepCounterB = 0;

void moveStraight(int stepsA, int stepsB, int speedA, int speedB) {
    stepCounterA = 0;
    stepCounterB = 0;
    int maxSteps = (stepsA > stepsB) ? stepsA : stepsB;
    for (int i = 0; i < maxSteps; i++) {
        if (i < stepsA) {
            // Simulate motor A step
            stepCounterA++;
        }
        if (i < stepsB) {
            // Simulate motor B step
            stepCounterB++;
        }
    }
}

void moveArc(int stepsA, int stepsB, int speedA, int speedB) {
    stepCounterA = 0;
    stepCounterB = 0;

    float stepRatioA = (float)stepsA / (stepsA + stepsB);
    float stepRatioB = (float)stepsB / (stepsA + stepsB);

    int totalSteps = stepsA + stepsB;

    for (int i = 0; i < totalSteps; i++) {
        if (i * stepRatioA < stepCounterA + 1 && stepCounterA < stepsA) {
            // Simulate motor A step
            stepCounterA++;
        }
        if (i * stepRatioB < stepCounterB + 1 && stepCounterB < stepsB) {
            // Simulate motor B step
            stepCounterB++;
        }
    }
}

int calculate_required_steps(float wanted_angle, int current_step) {
    float current_angle = current_step * STEP_ANGLE / MICRO_STEP;
    float diff_angle = wanted_angle - current_angle;
    while(diff_angle>180||diff_angle<-180)
    {
        if (diff_angle > 180) diff_angle -= 360;
        if (diff_angle < -180) diff_angle += 360;
    }
    int res = round(diff_angle*MICRO_STEP/STEP_ANGLE);
    return res;
}

