#include "unity.h"
#include "tcurve.h"

/* ______________________________________________________ */
/*  Test file specifically for TCurve module with TCurve
setting, testing of SCurve has to be done elsewhere

Author:     Martin Prokop
Date:       22.02.2025

List of tests:
    - Initialization test       (test_TCurve_InitializedProperly)
    - Acceleration set test     (test_TCurve_setAcceleration)
    - Max speed set test        (test_TCurve_setMaxVelocity)
    - Angle difference set test (test_SCurve_setDeltaPhi)

To be done:
    - Check values for velocity and acceleration given by
        get point method



*/
/* ______________________________________________________ */

TCurve *tcurve;

/* ______________________________________________________ */
/* Setup methods for all tests*/
void setUp(void)
{
    tcurve = new TCurve(TCurveType::SCurve);
}
void tearDown(void)
{
    delete tcurve;    // Free memory when done with the object
    tcurve = nullptr; // Optionally set the pointer to null to avoid dangling references
}
/* ______________________________________________________ */
/* Structes for parametrized tests*/
typedef struct
{
    TCurveError expected_error;
    float acceleration;
    float max_velocity;
    float delta_phi;
    float t_max;
    float t_mid;
} TCurveTestCase;

/* ______________________________________________________ */
/* Definition of tests*/
void test_TCurve_InitializedProperly(void)
{
    // Test if the TCurve is initialized with the expected values

    // 1. Check if the curve type is TCurve (expected default type)
    TEST_ASSERT_EQUAL(TCurveType::SCurve, tcurve->getCurveType()); // Assuming there's a getter for type

    // 2. Check if the default values for acceleration, max velocity, and delta_phi are zero
    // Assuming you have getter functions for each of these parameters
    TEST_ASSERT_EQUAL(0.0, tcurve->getAcceleration());
    TEST_ASSERT_EQUAL(0.0, tcurve->getMaxVelocity());
    TEST_ASSERT_EQUAL(0.0, tcurve->getDeltaPhi());
}

void test_TCurve_setAcceleration(void)
{
    /* Test if class reacts properly on acceleration set */
    TCurveTestCase test_cases[] = {
        {.expected_error = TCurveError::OK, .acceleration = 5.23f},
        {.expected_error = TCurveError::InvalidSetting, .acceleration = -1.0f}, // Negative value should fail
        {.expected_error = TCurveError::InvalidSetting, .acceleration = 0.0f}   // Boundary condition
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i)
    {
        TCurveError error = tcurve->setAcceleration(test_cases[i].acceleration);

        // Check if the error is as expected
        if (error != test_cases[i].expected_error)
        {
            char msg[50];
            snprintf(msg, sizeof(msg), "Expected error %d but got %d", test_cases[i].expected_error, error);
            TEST_FAIL_MESSAGE(msg);
        }

        // If the expected error was OK, check the acceleration value
        if (error == TCurveError::OK)
        {
            TEST_ASSERT_EQUAL(test_cases[i].acceleration, tcurve->getAcceleration());
        }
    }
}

void test_TCurve_setMaxVelocity(void)
{
    /* Test if class reacts properly on acceleration set */
    TCurveTestCase test_cases[] = {
        {.expected_error = TCurveError::OK, .max_velocity = 5.23f},
        {.expected_error = TCurveError::InvalidSetting, .max_velocity = -1.0f}, // Negative value should fail
        {.expected_error = TCurveError::InvalidSetting, .max_velocity = 0.0f}   // Boundary condition
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i)
    {
        TCurveError error = tcurve->setMaxVelocity(test_cases[i].max_velocity);

        // Check if the error is as expected
        if (error != test_cases[i].expected_error)
        {
            char msg[50];
            snprintf(msg, sizeof(msg), "Expected error %d but got %d", test_cases[i].expected_error, error);
            TEST_FAIL_MESSAGE(msg);
        }

        // If the expected error was OK, check the acceleration value
        if (error == TCurveError::OK)
        {
            TEST_ASSERT_EQUAL(test_cases[i].max_velocity, tcurve->getMaxVelocity());
        }
    }
}

void test_SCurve_setDeltaPhi(void)
{
    /* Test if class reacts properly on delta_phi set */
    TCurveTestCase test_cases[] = {
        {TCurveError::OK, .acceleration = 1.0f, .delta_phi = 1.0f, .t_max = 2},
        {TCurveError::OK, .acceleration = 1.0f, .delta_phi = -10.0f, .t_max = 6.3245553}
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i)
    {
        if (tcurve->setAcceleration(test_cases[i].acceleration) != TCurveError::OK)
        {
            TEST_FAIL_MESSAGE("Initialization failed during setting acceleration");
        };
        TCurveError error = tcurve->setDeltaPhi(test_cases[i].delta_phi);
        // Check if the error is as expected
        if (error != test_cases[i].expected_error)
        {
            char msg[50];
            snprintf(msg, sizeof(msg), "Expected error %d but got %d", test_cases[i].expected_error, error);
            TEST_FAIL_MESSAGE(msg);
        }
        if (error == TCurveError::OK)
        {
            TEST_ASSERT_FLOAT_WITHIN(0.001, test_cases[i].delta_phi,    tcurve->getDeltaPhi());
            TEST_ASSERT_FLOAT_WITHIN(0.001, test_cases[i].t_max,        tcurve->getTMax());
            TEST_ASSERT_FLOAT_WITHIN(0.001, test_cases[i].t_max/2,      tcurve->getTMid());
        }
    }
}

int main(void)
{
    UNITY_BEGIN();
    // Call test functions here
    RUN_TEST(test_TCurve_InitializedProperly);
    RUN_TEST(test_TCurve_setAcceleration);
    RUN_TEST(test_TCurve_setMaxVelocity);
    RUN_TEST(test_SCurve_setDeltaPhi);
    return UNITY_END();
}