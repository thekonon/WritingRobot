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

#include <stddef.h>  // For size_t
#include <cstdlib>  // For malloc and free
#include <stdexcept> // For exceptions (optional, if using C++)

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
    OK,
    NotOk,
    InvalidSetting,
    NotAValidCurveType,
    MustBeNonZeroFinite,
    TimeOutOfRange,
    NotImplemented
};

// Class for TCurve
class TCurve {
public:
    // Constructor and Destructor
    TCurve(TCurveType type);
    ~TCurve();

    // Methods for configuring the curve
    TCurveError set_acceleration(float acceleration);
    TCurveError set_max_velocity(float max_velocity);
    TCurveError set_phi(float delta_phi);

    // Method to get a point on the curve at a given time
    TCurveError get_point(float t, float& x_out);

    // Property getters
    TCurveType get_curve_type();
    float get_acceleration();
    float get_max_velocity();
    float get_phi();

private:
    TCurveError recalculate_internal_variables();

    TCurveType type;        // TCurve or SCurve
    float acceleration;    // A_MAX
    float max_velocity;    // W_MAX
    float delta_phi;       // ΔX
};

/* _____________________________________________________________________*/

#ifdef __cplusplus
}
#endif

#endif // TCURVE_H
