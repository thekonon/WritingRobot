#include "unity.h"
#include "tcurve.h"

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
    TEST_ASSERT_EQUAL(TCurveType::SCurve, tcurve->get_curve_type()); // Assuming there's a getter for type

    // 2. Check if the default values for acceleration, max velocity, and delta_phi are zero
    // Assuming you have getter functions for each of these parameters
    TEST_ASSERT_EQUAL(0.0, tcurve->get_acceleration());
    TEST_ASSERT_EQUAL(0.0, tcurve->get_max_velocity());
    TEST_ASSERT_EQUAL(0.0, tcurve->get_delta_phi());
}

void test_TCurve_set_acceleration(void)
{
    /* Test if class reacts properly on acceleration set */
    TCurveTestCase test_cases[] = {
        {.expected_error = TCurveError::OK, .acceleration = 5.23f},
        {.expected_error = TCurveError::InvalidSetting, .acceleration = -1.0f}, // Negative value should fail
        {.expected_error = TCurveError::InvalidSetting, .acceleration = 0.0f}   // Boundary condition
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i)
    {
        TCurveError error = tcurve->set_acceleration(test_cases[i].acceleration);

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
            TEST_ASSERT_EQUAL(test_cases[i].acceleration, tcurve->get_acceleration());
        }
    }
}

void test_TCurve_set_max_velocity(void)
{
    /* Test if class reacts properly on acceleration set */
    TCurveTestCase test_cases[] = {
        {.expected_error = TCurveError::OK, .max_velocity = 5.23f},
        {.expected_error = TCurveError::InvalidSetting, .max_velocity = -1.0f}, // Negative value should fail
        {.expected_error = TCurveError::InvalidSetting, .max_velocity = 0.0f}   // Boundary condition
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i)
    {
        TCurveError error = tcurve->set_max_velocity(test_cases[i].max_velocity);

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
            TEST_ASSERT_EQUAL(test_cases[i].max_velocity, tcurve->get_max_velocity());
        }
    }
}

void test_SCurve_set_delta_phi(void) // Remove the parameter
{
    /* Test if class reacts properly on delta_phi set */
    TCurveTestCase test_cases[] = {
        {TCurveError::OK, .acceleration = 10.0f, .delta_phi = 5.32f},
        {TCurveError::OK, .acceleration = 10.0f, .delta_phi = -10.0f}
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i)
    {
        if (tcurve->set_acceleration(test_cases[i].acceleration) != TCurveError::OK)
        {
            TEST_FAIL_MESSAGE("Initialization failed");
        };
        TCurveError error = tcurve->set_delta_phi(test_cases[i].delta_phi);
        // Check if the error is as expected
        if (error != test_cases[i].expected_error)
        {
            char msg[50];
            snprintf(msg, sizeof(msg), "Expected error %d but got %d", test_cases[i].expected_error, error);
            TEST_FAIL_MESSAGE(msg);
        }
        if (error == TCurveError::OK)
        {
            TEST_ASSERT_FLOAT_WITHIN(0.001, test_cases[i].delta_phi, tcurve->get_delta_phi());
        }
    }
}

int main(void)
{
    UNITY_BEGIN();
    // Call test functions here
    RUN_TEST(test_TCurve_InitializedProperly);
    RUN_TEST(test_TCurve_set_acceleration);
    RUN_TEST(test_TCurve_set_max_velocity);
    RUN_TEST(test_SCurve_set_delta_phi);
    return UNITY_END();
}