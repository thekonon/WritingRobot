#include <stdio.h>
#include "TCurve.h"

int main()
{
    printf("Working\n");
    
    TCurve curve;
    
    TCurve_init(&curve, 100.0f, 50.0f);
    
    TCurve_set_phi(&curve, 10.0f);

    float start_time = 0.0f;
    float end_time = 2.0f;

    if (TCurve_export_curve_to_csv(&curve, start_time, end_time, "curve_points_x.csv") == CURVE_OK)
    {
        printf("Exported curve points to curve_points.csv\n");
    }
    else
    {
        printf("Failed to export curve points.\n");
    }

    TCurve_set_phi(&curve, 20.0f);

    if (TCurve_export_curve_to_csv(&curve, start_time, end_time, "curve_points_y.csv") == CURVE_OK)
    {
        printf("Exported curve points to curve_points.csv\n");
    }
    else
    {
        printf("Failed to export curve points.\n");
    }
    
    return 0;
}
