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
#include <stddef.h>  // For size_t
#include <cstdlib>  // For malloc and free
#include <stdexcept> // For exceptions (optional, if using C++)
#include <math.h>

#ifdef __cplusplus
extern "C" {
#endif
/* _____________________________________________________________________*/

// Enum for curve type selection
enum class TCurveType {
    TCurve,
    SCurve
};

// Enum for error handling in TCurve operations
enum class TCurveError {
    OK,                     // 0
    NotOk,                  // 1
    InvalidSetting,         // 2
    NotAValidCurveType,     // 3
    MustBeNonZeroFinite,    // 4
    TimeOutOfRange,         // 5
    NotImplemented          // 6
};

// Class for TCurve
class TCurve {
public:
    // Constructor and Destructor
    TCurve(TCurveType type);
    ~TCurve();

    // Methods for configuring the curve
    TCurveError setAcceleration(float acceleration);
    TCurveError setMaxVelocity(float max_velocity);
    TCurveError setDeltaPhi(float delta_phi);

    // Method to get a point on the curve at a given time
    TCurveError getPoint(float t, float* x_out);

    // Property getters
    TCurveType getCurveType();
    float getAcceleration();
    float getMaxVelocity();
    float getDeltaPhi();
    float getTMax();
    float getTMid();
    float getWMax();

private:
    TCurveError recalculateInternalVariables();
    TCurveError getPointSCurve(float, float*);

    TCurveType type;        // TCurve or SCurve
    float acceleration;    // A_MAX
    float max_velocity;    // W_MAX
    float delta_phi;       // DX - its unsigned version
    int8_t sign;            // 1 / -1

    float t_mid;
    float t_max;
    float w_max;
};

/* _____________________________________________________________________*/

#ifdef __cplusplus
}
#endif

#endif // TCURVE_H
