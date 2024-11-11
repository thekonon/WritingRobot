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
TCurve::TCurve(TCurveType type) : type(type), acceleration(0), max_velocity(0), delta_phi(0){
    // Implementation provided by users
}

// Destructor
TCurve::~TCurve() {
    // Implementation provided by user
}

// Method to set acceleration
TCurveError TCurve::set_acceleration(float acceleration) {
    if (acceleration <= 0) return TCurveError::InvalidSetting;
    this->acceleration = acceleration;
    return TCurveError::OK;
}

// Method to set maximum velocity
TCurveError TCurve::set_max_velocity(float max_velocity) {
    if (max_velocity <= 0) return TCurveError::InvalidSetting;
    this->max_velocity = max_velocity;
    return TCurveError::OK;
}

// Method to set delta_phi
TCurveError TCurve::set_phi(float delta_phi) {
    // Implementation provided by user
    return TCurveError::NotImplemented;
}

// Method to get a point on the curve
TCurveError TCurve::get_point(float t, float& x_out) {
    // Implementation provided by user
    return TCurveError::NotImplemented;
}
float TCurve::get_acceleration() {
    return acceleration;
}
TCurveType TCurve::get_curve_type() {
    return type;
}

float TCurve::get_max_velocity() {
    return max_velocity;
}

float TCurve::get_phi() {
    return delta_phi;
}