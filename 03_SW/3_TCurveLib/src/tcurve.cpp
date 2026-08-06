#include "../inc/tcurve.h"

// ----------------------------------------------------------------------
// File: TCurve.cpp
// Author: Martin Prokop
// Description: Implementation file for TCurve class, providing curve
//              configuration and evaluation methods compatible with STM32.
//
// Date Created: 10.11.2024
// Last Modified: 30.03.2025
// Version: 2.0
//
// Notes:
//   - SCurve is no longer supported, TCurve will do both functionality
// ----------------------------------------------------------------------

/**
 *   @brief Constructor for TCurve library
 *   @param None
 */
TCurve::TCurve()
{
    this->max_acceleration = 0.0f;
    this->max_velocity = 0.0f;
    this->resetInternalVariables();
}

/**
 *   @brief Destructor for TCurve library
 *   @param None
 */
TCurve::~TCurve() {}

/**
 * @brief Sets maximal allowed acceleration
 * @param max_accelearation (float)
 * @return TCurveError
 */
TCurveError TCurve::setAcceleration(float max_acceleration)
{
    if (max_acceleration < 0.001)
    {
        /*Maximal acceleration too small or negative*/
        return TCurveError::InvalidSetting;
    }
    this->max_acceleration = max_acceleration;
    this->needs_to_be_recalc = 1;
    this->recalculateInternalVariables();
    return TCurveError::OK;
}

TCurveError TCurve::setMaxVelocity(float max_velocity)
{
    if (max_velocity < 0.001)
    {
        /*Maximal acceleration too small or negative*/
        return TCurveError::InvalidSetting;
    }
    this->max_velocity = max_velocity;
    this->needs_to_be_recalc = 1;
    this->recalculateInternalVariables();
    return TCurveError::OK;
}
/**
 * @brief Set angle difference
 * @param deltaPhi (float)
 */
TCurveError TCurve::setDeltaPhi(float delta_phi)
{
    this->resetInternalVariables();
    if (delta_phi > 0)
    {
        this->delta_phi = delta_phi;
        this->sign = 1;
    }
    else
    {
        this->delta_phi = -delta_phi;
        this->sign = -1;
    }
    this->needs_to_be_recalc = 1;
    this->recalculateInternalVariables();
    return TCurveError::OK;
}

/**
 * @brief Returns saved maximal acceleration
 * @return maximal accelaration (float)
 */
float TCurve::getAcceleration()
{
    return this->max_acceleration;
}

/**
 * @brief Returns saved maximal velocity
 * @return maximal velocity (float)
 */
float TCurve::getMaxVelocity()
{
    return this->max_velocity;
}

/**
 * @brief Returns saved maximal angle difference
 * @return Angle difference (float)
 */
float TCurve::getDeltaPhi()
{
    return this->delta_phi * this->sign;
}

/**
 *   @brief Return a type of curve (TCurve, SCurve)
 *   @param None
 *   @return TCurveType
 */
TCurveType TCurve::getCurveType()
{
    return this->type;
}

float TCurve::getT1()
{
    return this->t_1;
}

float TCurve::getT2()
{
    return this->t_2;
}

float TCurve::getTMax()
{
    return this->t_max;
}

float TCurve::getWMax()
{
    return this->w_max;
}

/**
 * @brief Saves a result in x_out, returns if calculation was ok
 * for given time time
 *
 */
TCurveError TCurve::getPoint(float time, float *x_out)
{
    /* Check if the internal variables are recalculated*/
    if (this->needs_to_be_recalc == 1)
    {
        TCurveError result = this->recalculateInternalVariables();
        if (result == TCurveError::NotInitialized)
        {
            return TCurveError::NotInitialized;
        }
    }
    if (this->type == TCurveType::NotInitialized)
    {
        return TCurveError::NotInitialized;
    }
    if (this->type == TCurveType::SCurve)
    {
        *x_out = getSCurvePoint(time);
    }
    if (this->type == TCurveType::TCurve)
    {
        *x_out = getTCurvePoint(time);
    }

    return TCurveError::OK;
}

/**
 * @brief Recalculates internal variables such as times and other constants
 */
TCurveError TCurve::recalculateInternalVariables()
{
    if (this->getAcceleration() == 0.0f)
    {
        return TCurveError::NotInitialized;
    }
    if (this->getDeltaPhi() == 0.0f)
    {
        return TCurveError::NotInitialized;
    }

    float v, dp, a;
    v = this->getMaxVelocity();
    dp = this->getDeltaPhi();
    a = this->getAcceleration();
    /* SCurve / TCurve condition */
    bool cond1 = (v * v - dp * a > 0);
    bool cond2 = (v == 0.0f);
    if (cond1 || cond2)
    {
        /* In this case its SCurve*/
        this->type = TCurveType::SCurve;
        this->t_1 = sqrtf(dp / a);
        this->t_2 = this->t_1;
        this->t_max = 2 * this->t_1;
        this->w_max = a * this->t_1;
    }
    else
    {
        /* In this case its TCurve*/
        this->type = TCurveType::TCurve;
        this->t_1 = v / a;
        this->t_2 = dp / v;
        this->t_max = (v * v + a * dp) / (a * v);
        this->w_max = a * this->t_1;
        /* Constants */
        this->constants[0] = 0;
        this->constants[1] = 0;
        this->constants[2] = v;
        this->constants[3] = -v*v/(2*a);
        this->constants[4] = (v*v+a*dp)/v;
        this->constants[5] = -(a*a*dp*dp+v*v*v*v)/(2*a*v*v);
    }
    this->needs_to_be_recalc = 0;
    return TCurveError::OK;
}

/**
 * @brief Resets internal variables calculated based on 
 * selected maximal acceleration, velocity and angle diff
 * @param None
 * @return TCurveError
 */
TCurveError TCurve::resetInternalVariables()
{
    this->delta_phi = 0.0f;
    this->sign = 1;
    this->type = TCurveType::NotInitialized;
    this->t_1 = 0;
    this->t_2 = 0;
    this->t_max = 0;
    this->w_max = 0;
    this->needs_to_be_recalc = 1;
    for(int i = 0; i < 6; i++)
    {
        this->constants[i] = 0;
    }
    return TCurveError::OK;
}

/**
 * @brief Returns value for given time assuming the curve is SCurve and it is initialized
 * @param time(float): given time
 * @returns value(float|NAN): calculated value, NAN for invalid times
 */
float TCurve::getSCurvePoint(float time)
{
    if(time < 0 || time > this->t_max)
    {
        return NAN;
    }
    if (time < this->getT1())
    {
        return (this->getAcceleration() * time * time / 2) * this->sign;
    }
    {
        float new_time = this->t_max - time;
        return (this->getDeltaPhi() - this->getAcceleration() * new_time * new_time / 2) * this->sign;
    }
}

/**
 * @brief Returns value for given time assuming curve is TCurve and it is initialized
 * @param time(float)
 */
 float TCurve::getTCurvePoint(float time)
 {
    if(time < 0 || time > this->t_max)
    {
        return NAN;
    }
    if(time <= this->getT1())
    {
        return this->getAcceleration()*time*time/2+this->constants[0]*time+this->constants[1];
    }
    if(time <= this->getT2())
    {
        return this->constants[2]*time+this->constants[3];
    }
    if(time <= this->getTMax())
    {
        return -this->getAcceleration()*time*time/2+((this->constants[4])*time)+(this->constants[5]);
    }
    return NAN;
 }
