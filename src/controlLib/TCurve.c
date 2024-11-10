#include "TCurve.h"

void TCurve_init(TCurve* curve, float a_max, float w_max)
{
    curve->A_MAX = a_max;
    curve->W_MAX = w_max;
    curve->DT = 1e-2;  // Time division in seconds
    curve->phi_diff = 0;
}

CurveState TCurve_set_phi(TCurve* curve, float phi)
{
    curve->phi_diff = phi;
    printf("curve: %.2f\n", curve->phi_diff);

    float phi_max_s_curve = curve->W_MAX * curve->W_MAX / (2 * curve->A_MAX);
    if (phi < phi_max_s_curve)
    {   
        printf("S_curve");
        curve->curve_type = S_CURVE;
        curve->mid_time_point = sqrt((curve->phi_diff / 2) / curve->A_MAX * 2);
        curve->k_max = round(2 * curve->mid_time_point / curve->DT);
    }
    else
    {
        printf("T_curve");
        curve->curve_type = T_CURVE;
        curve->mid_time_point = curve->W_MAX / curve->A_MAX;
        curve->phi_s_curve = curve->W_MAX * curve->W_MAX / curve->A_MAX;
        float linear_part = curve->phi_diff - curve->phi_s_curve;
        float linear_part_time = linear_part / curve->W_MAX;
        curve->linear_part_time_end = curve->mid_time_point + linear_part_time;
        float phi_s_curve_time = 2 * curve->W_MAX / curve->A_MAX;
        float total_time = phi_s_curve_time + linear_part_time;
        curve->k_max = round(total_time / curve->DT);
    }
    return CURVE_OK;
}

CurveState TCurve_curve_point(TCurve* curve, float time, float* value)
{
    if (curve->curve_type == S_CURVE)
    {
        if (time <= curve->mid_time_point)
            *value = curve->A_MAX * time * time / 2;
        else
            *value = curve->phi_diff - curve->A_MAX * (2 * curve->mid_time_point - time) * (2 * curve->mid_time_point - time) / 2;
        return CURVE_OK;
    }
    else if (curve->curve_type == T_CURVE)
    {
        if (time <= curve->mid_time_point)
            *value = curve->A_MAX * time * time / 2;
        else if (time <= curve->linear_part_time_end)
            *value = curve->phi_s_curve / 2 + (time - curve->mid_time_point) * curve->W_MAX;
        else
            *value = curve->phi_diff - curve->A_MAX * (curve->mid_time_point - (time - curve->linear_part_time_end)) * (curve->mid_time_point - (time - curve->linear_part_time_end)) / 2;
        return CURVE_OK;
    }
    return CURVE_NOT_OK;
}

CurveState TCurve_export_curve_to_csv(TCurve* curve, float start_time, float end_time, const char* filename)
{
    if (start_time < 0 || end_time > curve->k_max * curve->DT || start_time >= end_time)
        return CURVE_NOT_OK;

    FILE* file = fopen(filename, "w");
    if (!file)
        return CURVE_NOT_OK;

    fprintf(file, "Time,Value\n");

    for (float t = start_time; t <= end_time; t += curve->DT)
    {
        float value;
        if (TCurve_curve_point(curve, t, &value) == CURVE_OK)
        {
            fprintf(file, "%f,%f\n", t, value);
        }
        else
        {
            fclose(file);
            return CURVE_NOT_OK;
        }
    }
    fclose(file);
    return CURVE_OK;
}

float TCurve_get_DT(TCurve* curve) {
    return curve->DT;
}

int TCurve_get_k_max(TCurve* curve) {
    return curve->k_max;
}
