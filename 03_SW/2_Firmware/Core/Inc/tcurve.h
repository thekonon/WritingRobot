#ifndef TCURVE_H
#define TCURVE_H

// ----------------------------------------------------------------------
// File: TCurve.h
// Author: theKonon
// Description:
//
// Date Created: 10.11.2024
// Last Modified: 10.11.2024
// Version: 1.0
//
// Notes:
//   -
// ----------------------------------------------------------------------
#include <stdint.h>
#include <stddef.h> // For size_t
// #include <cstdlib>          // For malloc and free
// #include <stdexcept>        // For exceptions (optional, if using C++)
#include <math.h>

#ifdef __cplusplus
extern "C"
{
#endif
    /* _____________________________________________________________________*/

    // Enum for curve type selection @curve_type_definition
    enum class TCurveType
    {
        TCurve,
        SCurve,
        NotInitialized
    };

    // Enum for error handling in TCurve operations
    enum class TCurveError
    {
        OK,                  // 0
        NotOk,               // 1
        InvalidSetting,      // 2
        MustBeNonZeroFinite, // 3
        TimeOutOfRange,      // 4
        NotImplemented,      // 5
        NotInitialized       // 6
    };

    /* _____________________________________________ */

    // Class for TCurve
    class TCurve
    {
    public:
        // Constructor and Destructor
        TCurve();
        ~TCurve();

        // Methods for configuring the curve
        TCurveError setAcceleration(float max_acceleration);
        TCurveError setMaxVelocity(float max_velocity);
        TCurveError setDeltaPhi(float delta_phi);

        // Method to get a point on the curve at a given time
        TCurveError getPoint(float t, float *x_out);

        TCurveError recalculateInternalVariables();

        // Property getters
        TCurveType getCurveType();
        float getAcceleration();
        float getMaxVelocity();
        float getDeltaPhi();
        float getT1();
        float getT2();
        float getTMax();
        float getWMax();

    private:
        TCurveError resetInternalVariables();
        float       getSCurvePoint(float time);
        float       getTCurvePoint(float time);

        TCurveType type;            // TCurve / SCurve or uninitilized
        float max_acceleration;     // A_MAX
        float max_velocity;         // W_MAX
        float delta_phi;            // DX - its unsigned version
        int8_t sign;                // 1 / -1
        uint8_t needs_to_be_recalc; // 0 / 1

        float t_1;
        float t_2;
        float t_max;
        float w_max;
        float constants[6];
    };

    /* _____________________________________________________________________*/

#ifdef __cplusplus
}
#endif

#endif // TCURVE_H
