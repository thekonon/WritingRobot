#ifndef ROBOT_H
#define ROBOT_H

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "TCurve.h"

// Class definition for Robot
class Robot {
public:
    float A_MAX;
    float W_MAX;
    const float DT = 0.01;
    float phi_needed;
    float *phi_vals = nullptr;
    TCurve tcurve;

    Robot(float a_max, float w_max);
    ~Robot();
    void recalculate(float phi_needed);
    void print_info();
    void save_info(const char* file_name);

private:
    void allocate_vector(int k);
};

#endif // ROBOT_H
