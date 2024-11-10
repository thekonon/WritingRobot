#ifndef TCURVE_H
#define TCURVE_H

#include <stdio.h>
#include <math.h>
#include <stdlib.h>

// Enum for curve state
typedef enum {
    CURVE_NOT_OK = 0,
    CURVE_OK = 1
} CurveState;

// Enum for curve type
typedef enum {
    S_CURVE = 0,
    T_CURVE = 1
} CurveType;

// Structure for TCurve
typedef struct {
    float A_MAX;
    float W_MAX;
    float DT;
    int k_max;
    
    float phi_diff;
    float mid_time_point;
    float phi_s_curve;
    float linear_part_time_end;
    CurveType curve_type;
} TCurve;

// Function prototypes
void TCurve_init(TCurve* curve, float a_max, float w_max);
CurveState TCurve_set_phi(TCurve* curve, float phi);
CurveState TCurve_curve_point(TCurve* curve, float time, float* value);
CurveState TCurve_export_curve_to_csv(TCurve* curve, float start_time, float end_time, const char* filename);

float TCurve_get_DT(TCurve* curve);
int TCurve_get_k_max(TCurve* curve);

#endif // TCURVE_H
