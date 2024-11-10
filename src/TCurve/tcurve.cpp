#include "TCurve.h"

// ----------------------------------------------------------------------
// File: TCurve.cpp
// Author: Martin Prokop
// Description: Implementation file for TCurve class, providing curve
//              configuration and evaluation methods compatible with STM32.
// 
// Date Created: 10.11.2024
// Last Modified: 10.11.2024
// Version: 1.0
//
// Notes:
//   - 
// ----------------------------------------------------------------------

// Constructor
TCurve::TCurve(TCurveType type) : type_(type), acceleration_(0), max_velocity_(0), phi_(0){
    // Implementation provided by user
}

// Destructor
TCurve::~TCurve() {
    // Implementation provided by user
}

// Method to set acceleration
TCurveError TCurve::set_acceleration(double acceleration) {
    // Implementation provided by user
    return TCurveError::NotImplemented;
}

// Method to set maximum velocity
TCurveError TCurve::set_max_velocity(double max_velocity) {
    // Implementation provided by user
    return TCurveError::NotImplemented;
}

// Method to set phi
TCurveError TCurve::set_phi(double phi) {
    // Implementation provided by user
    return TCurveError::NotImplemented;
}

// Method to get a point on the curve
TCurveError TCurve::get_point(double t, double& x_out) {
    // Implementation provided by user
    return TCurveError::NotImplemented;
}
float TCurve::get_acceleration() {
    return acceleration_;
}
TCurveType TCurve::getType() {
    return type_;
}

float TCurve::get_max_velocity() {
    return max_velocity_;
}

float TCurve::get_phi() {
    return phi_;
}