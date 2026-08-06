#include "tcurve.h"
#include <string>
#include <iostream>

/* ______________________________________________________ */
/*  Test file specifically for TCurve module

Author:     thekonon
Date:       22.02.2025

List of tests:
    - Initialization test       (test_TCurve_InitializedProperly)
    - Acceleration set test     (test_TCurve_setAcceleration)
    - Max speed set test        (test_TCurve_setMaxVelocity)
    - Angle difference set test (test_TCurve_setDeltaPhi)

To be done:
    - Check values for velocity and max_acceleration given by
        get point method
    - Check if right curve type was selected
*/
/* ______________________________________________________ */

TCurve tCurve;

int main()
{

    float maxAcceleration = 20.0f;
    float maxVelocity = 10.0f;
    float deltaPhi = 10.0f;

    std::cout << "----------------------------------------------------" << std::endl;
    std::cout << "|    Runninng the analysis" << std::endl;
    std::cout << "----------------------------------------------------" << std::endl;

    if (tCurve.setAcceleration(maxAcceleration) != TCurveError::OK)
    {
        std::cout << "Invalid max acceleration settings" << std::endl;
        return 1;
    };

    if (tCurve.setMaxVelocity(maxVelocity) != TCurveError::OK)
    {
        std::cout << "Invalid max velocity settings" << std::endl;
        return 1;
    };

    if (tCurve.setDeltaPhi(deltaPhi) != TCurveError::OK)
    {
        std::cout << "Invalid delta phi" << std::endl;
        return 1;
    };

    std::string curveType;

    switch (tCurve.getCurveType())
    {
    case TCurveType::TCurve:
        curveType = "TCurve";
        break;
    case TCurveType::SCurve:
        curveType = "SCurve";
        break;
    default:
        std::cout << "Curve is not initialized" << std::endl;
    }

    std::cout << "|    Curve type: "<< curveType << std::endl;

    

    std::cout << "Running the analysis" << std::endl;
    return 0;
}