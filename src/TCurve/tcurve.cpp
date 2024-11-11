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
TCurve::TCurve(TCurveType type) : type(type), acceleration(0), max_velocity(0), delta_phi(0), t_mid(0), t_max(0), w_max(0)
{
    // Implementation provided by users
}

// Destructor
TCurve::~TCurve()
{
    // Implementation provided by user
}

// Method to set acceleration
TCurveError TCurve::set_acceleration(float acceleration)
{
    if (acceleration <= 0)
        return TCurveError::InvalidSetting;
    this->acceleration = acceleration;
    return TCurveError::OK;
}

// Method to set maximum velocity
TCurveError TCurve::set_max_velocity(float max_velocity)
{
    if (max_velocity <= 0)
        return TCurveError::InvalidSetting;
    this->max_velocity = max_velocity;
    return TCurveError::OK;
}

// Method to set delta_phi
TCurveError TCurve::set_delta_phi(float delta_phi)
{
    if (delta_phi == 0)
        return TCurveError::MustBeNonZeroFinite;
    if (get_acceleration() == 0)
        return TCurveError::InvalidSetting;
    if (get_max_velocity() == 0 && get_curve_type() == TCurveType::TCurve)
    {
        return TCurveError::InvalidSetting;
    }
    if (delta_phi > 0)
    {
        sign = 1;
        this->delta_phi = delta_phi;
    }
    else
    {
        sign = -1;
        this->delta_phi = -delta_phi;
    }

    TCurveError error = recalculate_internal_variables();

    switch (error)
    {
    case TCurveError::OK:
        return TCurveError::OK;
        break;

    default:
        return TCurveError::NotOk;
    }
}

// Method to get a point on the curve
TCurveError TCurve::get_point(float t, float &x_out)
{
    // Implementation provided by user
    return TCurveError::NotImplemented;
}
float TCurve::get_acceleration()
{
    return acceleration;
}
TCurveType TCurve::get_curve_type()
{
    return type;
}

float TCurve::get_max_velocity()
{
    return max_velocity;
}

float TCurve::get_delta_phi()
{
    return delta_phi*sign;
}

TCurveError TCurve::recalculate_internal_variables()
{
    // delta phi is unsigned - therefore have to be used
    t_mid = sqrt(delta_phi / get_acceleration());
    if (isnan(t_mid))
    {
        return TCurveError::NotOk;
    }
    t_max = t_mid * 2;
    w_max = t_mid * get_acceleration();
    return TCurveError::OK;
}