#include "unity.h"
#include "tcurve.h"

TCurve* tcurve;

void setUp(void) 
{
    tcurve = new TCurve(TCurveType::TypeTCurve);
}
void tearDown(void) 
{
    delete tcurve;  // Free memory when done with the object
    tcurve = nullptr;  // Optionally set the pointer to null to avoid dangling references
}

void test_TCcurve_InitializedProperly(void) {
    // Test if the TCurve is initialized with the expected values

    // 1. Check if the curve type is TCurve (expected default type)
    TEST_ASSERT_EQUAL(TCurveType::TypeTCurve, tcurve->getType()); // Assuming there's a getter for type

    // 2. Check if the default values for acceleration, max velocity, and phi are zero
    // Assuming you have getter functions for each of these parameters
    TEST_ASSERT_EQUAL(0.0, tcurve->get_acceleration());
    TEST_ASSERT_EQUAL(0.0, tcurve->get_max_velocity());
    TEST_ASSERT_EQUAL(0.0, tcurve->get_phi());
}


int main(void) {
    UNITY_BEGIN();
    // Call test functions here
    RUN_TEST(test_TCcurve_InitializedProperly);
    return UNITY_END();
}