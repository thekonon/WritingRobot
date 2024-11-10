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
    TypeTCurve,
    TypeSCurve
};

// Enum for error handling in TCurve operations
enum class TCurveError {
    OK,
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
    TCurveError set_acceleration(double acceleration);
    TCurveError set_max_velocity(double max_velocity);
    TCurveError set_phi(double phi);

    // Method to get a point on the curve at a given time
    TCurveError get_point(double t, double& x_out);

    TCurveType getType();
    float get_acceleration();
    float get_max_velocity();
    float get_phi();

private:
    // Private members to store configuration parameters
    TCurveType type_;
    double acceleration_;
    double max_velocity_;
    double phi_;
};

/* _____________________________________________________________________*/

#ifdef __cplusplus
}
#endif

#endif // TCURVE_H
