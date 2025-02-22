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
TCurveError TCurve::setAcceleration(float acceleration)
{
    if (acceleration <= 0)
        return TCurveError::InvalidSetting;
    this->acceleration = acceleration;
    return TCurveError::OK;
}

// Method to set maximum velocity
TCurveError TCurve::setMaxVelocity(float max_velocity)
{
    if (max_velocity <= 0)
        return TCurveError::InvalidSetting;
    this->max_velocity = max_velocity;
    return TCurveError::OK;
}

// Method to set delta_phi
TCurveError TCurve::setDeltaPhi(float delta_phi)
{
    if (delta_phi == 0)
        return TCurveError::MustBeNonZeroFinite;
    if (getAcceleration() == 0)
        return TCurveError::InvalidSetting;
    if (getMaxVelocity() == 0 && getCurveType() == TCurveType::TCurve)
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

    TCurveError error = recalculateInternalVariables();

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
TCurveError TCurve::getPoint(float t, float* x_out)
{
    // Implementation provided by user
    return TCurveError::NotOk;
}
float TCurve::getAcceleration()
{
    return acceleration;
}
TCurveType TCurve::getCurveType()
{
    return type;
}

float TCurve::getMaxVelocity()
{
    return max_velocity;
}

float TCurve::getDeltaPhi()
{
    /* Returne delta_phi with its sign*/
    return delta_phi * sign;
}

float TCurve::getTMax()
{
    return t_max;
}
float TCurve::getTMid()
{
    return t_mid;
}
float TCurve::getWMax()
{
    return w_max;
}

TCurveError TCurve::recalculateInternalVariables()
{
    // delta phi is unsigned - therefore have to be used
    t_mid = sqrt(delta_phi / getAcceleration());
    if (isnan(t_mid))
    {
        return TCurveError::NotOk;
    }
    t_max = t_mid * 2;
    w_max = t_mid * getAcceleration();
    return TCurveError::OK;
}