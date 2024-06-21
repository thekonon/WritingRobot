#include "motor_control.h"
#include "constants.h"
#include "math.h"

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

