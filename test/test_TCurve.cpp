#include "unity.h"
#include "tcurve.h"

TCurve* tcurve;

/* ______________________________________________________ */
/* Setup methods for all tests*/
void setUp(void) 
{
    tcurve = new TCurve(TCurveType::TCurve);
}
void tearDown(void) 
{
    delete tcurve;  // Free memory when done with the object
    tcurve = nullptr;  // Optionally set the pointer to null to avoid dangling references
}
/* ______________________________________________________ */
/* Structes for parametrized tests*/
typedef struct {
    float test_value;
    TCurveError expected_error;
    float expected_acceleration;
} AccelerationTestCase;
/* ______________________________________________________ */
/* Definition of tests*/
void test_TCcurve_InitializedProperly(void) {
    // Test if the TCurve is initialized with the expected values

    // 1. Check if the curve type is TCurve (expected default type)
    TEST_ASSERT_EQUAL(TCurveType::TCurve, tcurve->get_curve_type()); // Assuming there's a getter for type

    // 2. Check if the default values for acceleration, max velocity, and delta_phi are zero
    // Assuming you have getter functions for each of these parameters
    TEST_ASSERT_EQUAL(0.0, tcurve->get_acceleration());
    TEST_ASSERT_EQUAL(0.0, tcurve->get_max_velocity());
    TEST_ASSERT_EQUAL(0.0, tcurve->get_phi());
}

void test_TCurve_set_acceleration(void)
{
    /* Test if class reacts properly on acceleration set */
    AccelerationTestCase test_cases[] = {
        {5.23f, TCurveError::OK, 5.23f},
        {-1.0f, TCurveError::InvalidSetting, 0.0f}, // Negative value should fail
        {0.0f, TCurveError::InvalidSetting, 0.0f}   // Boundary condition
    };

    for (size_t i = 0; i < sizeof(test_cases) / sizeof(test_cases[0]); ++i) {
        TCurveError error = tcurve->set_acceleration(test_cases[i].test_value);
        
        // Check if the error is as expected
        if (error != test_cases[i].expected_error) {
            char msg[50];
            snprintf(msg, sizeof(msg), "Expected error %d but got %d", test_cases[i].expected_error, error);
            TEST_FAIL_MESSAGE(msg);
        }

        // If the expected error was OK, check the acceleration value
        if (error == TCurveError::OK) {
            TEST_ASSERT_EQUAL(test_cases[i].expected_acceleration, tcurve->get_acceleration());
        }
    }
}


int main(void) {
    UNITY_BEGIN();
    // Call test functions here
    RUN_TEST(test_TCcurve_InitializedProperly);
    RUN_TEST(test_TCurve_set_acceleration);
    return UNITY_END();
}