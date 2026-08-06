#include "unity.h"
#include "tcurve.h"
#include "stdlib.h"

/* ______________________________________________________ */
/*  Test file specifically for TCurve module

Author:     Martin Prokop
Date:       06.08.2026

List of tests:
    - Initialization test       (test_TCurve_InitializedProperly)
    - Acceleration set test     (test_TCurve_setAcceleration)
    - Max speed set test        (test_TCurve_setMaxVelocity)
    - Angle difference set test (test_TCurve_setDeltaPhi)

To be done:
    - Check values for velocity and max_acceleration given by
        get point method
    - Check if right curve type was selected
*/
/* ______________________________________________________ */

TCurve *tCurve;

/* ______________________________________________________ */
/* Setup methods for all tests*/
void setUp(void)
{
    tCurve = new TCurve();
    TEST_ASSERT_NOT_NULL(tCurve); // Ensure object was created
}
void tearDown(void)
{
    delete tCurve;    // Free memory when done with the object
    tCurve = nullptr; // Optionally set the pointer to null to avoid dangling references
}
/* ______________________________________________________ */
/* Definition of tests*/

/**
 * @brief Test if all property are initilized properly
 */
void test_TCurve_InitializedProperly(void)
{
    TEST_ASSERT_EQUAL_FLOAT(0.0f, tCurve->getAcceleration());
    TEST_ASSERT_EQUAL_FLOAT(0.0f, tCurve->getMaxVelocity());
    TEST_ASSERT_EQUAL_FLOAT(0.0f, tCurve->getDeltaPhi());

    TEST_ASSERT_EQUAL(TCurveType::NotInitialized, tCurve->getCurveType()); // Verify type
}

void test_TCurve_setAcceleration_positive()
{
    float test_acceleration = 12.35f;
    TCurveError result = tCurve->setAcceleration(test_acceleration);
    TEST_ASSERT_EQUAL(TCurveError::OK, result);
    TEST_ASSERT_EQUAL_FLOAT(test_acceleration, tCurve->getAcceleration());
}

void test_TCurve_setAcceleration_negative()
{
    float test_acceleration = -13.35f;
    TCurveError result = tCurve->setAcceleration(test_acceleration);
    TEST_ASSERT_EQUAL(TCurveError::InvalidSetting, result);
}

void test_TCurve_setMaxVelocity_positive()
{
    float test_velocity = 10.35f;
    TCurveError result = tCurve->setMaxVelocity(test_velocity);
    TEST_ASSERT_EQUAL(TCurveError::OK, result);
    TEST_ASSERT_EQUAL_FLOAT(test_velocity, tCurve->getMaxVelocity());
}

void test_TCurve_setMaxVelocity_negative()
{
    float test_velocity = -11.35f;
    TCurveError result = tCurve->setMaxVelocity(test_velocity);
    TEST_ASSERT_EQUAL(TCurveError::InvalidSetting, result);
}

void test_TCurve_setDeltaPhi_positive()
{
    float test_delta_phi = 1.234f;
    TCurveError result = tCurve->setDeltaPhi(test_delta_phi);
    TEST_ASSERT_EQUAL(TCurveError::OK, result);
    TEST_ASSERT_EQUAL_FLOAT(test_delta_phi, tCurve->getDeltaPhi());
}

void test_TCurve_setDeltaPhi_negative()
{
    float test_delta_phi = -2.234f;
    TCurveError result = tCurve->setDeltaPhi(test_delta_phi);
    TEST_ASSERT_EQUAL(TCurveError::OK, result);
    TEST_ASSERT_EQUAL_FLOAT(test_delta_phi, tCurve->getDeltaPhi());
}

void test_TCurve_recalculateInternalVariables_TCurve()
{
    tCurve->setDeltaPhi(20.0f);
    tCurve->setMaxVelocity(5.0f);
    tCurve->setAcceleration(20.0f);

    float test_result = 0.0f;
    TCurveError result = tCurve->getPoint(0, &test_result);

    TEST_ASSERT_EQUAL(TCurveError::OK, result);
    TEST_ASSERT_EQUAL(TCurveType::TCurve, tCurve->getCurveType());
    TEST_ASSERT_EQUAL_FLOAT(0.25f, tCurve->getT1());
    TEST_ASSERT_EQUAL_FLOAT(4.0f, tCurve->getT2());
    TEST_ASSERT_EQUAL_FLOAT(4.25f, tCurve->getTMax());
    TEST_ASSERT_EQUAL_FLOAT(5.0f, tCurve->getWMax());
}

void test_TCurve_recalculateInternalVariables_SCurve()
{
    tCurve->setDeltaPhi(20.0f);
    tCurve->setMaxVelocity(150.0f);
    tCurve->setAcceleration(10.0f);

    float test_result = 0.0f;
    TCurveError result = tCurve->getPoint(0, &test_result);

    TEST_ASSERT_EQUAL(TCurveError::OK, result);
    TEST_ASSERT_EQUAL(TCurveType::SCurve, tCurve->getCurveType());
    TEST_ASSERT_EQUAL_FLOAT(1.41421354f, tCurve->getT1());
    TEST_ASSERT_EQUAL_FLOAT(1.41421354f, tCurve->getT2());
    TEST_ASSERT_EQUAL_FLOAT(2.82842708f, tCurve->getTMax());
    TEST_ASSERT_EQUAL_FLOAT(14.1421356f, tCurve->getWMax());
}

void test_TCurve_getPoint_SCurve()
{
    tCurve->setDeltaPhi(20.0f);
    tCurve->setMaxVelocity(150.0f);
    tCurve->setAcceleration(10.0f);

    float time_points[] = {0.0f, 0.1f, 0.5f, 0.7f, 1.41421354f, 1.5f, 2.0f, 2.828f};
    float value_points[] = {0.000000f, 0.05f, 1.25f, 2.45f, 10.000000f, 11.176407f, 16.568542f, 20.000000f};

    uint8_t points_length = sizeof(time_points) / sizeof(time_points[0]);
    float calculated_point = 0;
    float *calculated_points = (float *)malloc(points_length * sizeof(float));
    if (calculated_points == NULL)
    {
        /* Allocation fail */
        TEST_FAIL_MESSAGE("Failed to allocate points vector");
    }
    /* Calculate points */
    for (int i = 0; i < points_length; i++)
    {
        tCurve->getPoint(time_points[i], &calculated_points[i]);
        printf("%ff, ", calculated_points[i]);
    }
    /* Test values */
    TEST_ASSERT_EQUAL_FLOAT_ARRAY(value_points, calculated_points, points_length);

    /* Deallocate memory */
    free(calculated_points);
}

void test_TCurve_getPoint_TCurve()
{
    tCurve->setDeltaPhi(20.0f);
    tCurve->setMaxVelocity(10.0f);
    tCurve->setAcceleration(10.0f);

    float time_points[] = {0.0f, 0.5f, 0.7f, 0.8f, 0.9f, 1.0f, 1.0f, 1.0f, 1.5f, 1.9f, 2.0f, 2.5f, 2.9f, 3.0f};
    float value_points[] = {0.000000f, 1.250000f, 2.450000f, 3.200000f, 4.050000f, 5.000000f, 5.000000f, 5.000000f, 10.000000f, 14.000000f, 15.000000f, 18.750000f, 19.949997f, 20.000000f};

    uint8_t points_length = sizeof(time_points) / sizeof(time_points[0]);
    float calculated_point = 0;
    float *calculated_points = (float *)malloc(points_length * sizeof(float));
    if (calculated_points == NULL)
    {
        /* Allocation fail */
        TEST_FAIL_MESSAGE("Failed to allocate points vector");
    }
    /* Calculate points */
    for (int i = 0; i < points_length; i++)
    {
        tCurve->getPoint(time_points[i], &calculated_points[i]);
    }

    /* Test values */
    TEST_ASSERT_EQUAL_FLOAT_ARRAY(value_points, calculated_points, points_length);

    /* Deallocate memory */
    free(calculated_points);
}

int main(void)
{
    UNITY_BEGIN();
    // Call test functions here
    RUN_TEST(test_TCurve_InitializedProperly);
    RUN_TEST(test_TCurve_setAcceleration_positive);
    RUN_TEST(test_TCurve_setAcceleration_negative);
    RUN_TEST(test_TCurve_setMaxVelocity_positive);
    RUN_TEST(test_TCurve_setMaxVelocity_negative);
    RUN_TEST(test_TCurve_setDeltaPhi_positive);
    RUN_TEST(test_TCurve_setDeltaPhi_negative);
    RUN_TEST(test_TCurve_recalculateInternalVariables_TCurve);
    RUN_TEST(test_TCurve_recalculateInternalVariables_SCurve);
    RUN_TEST(test_TCurve_getPoint_SCurve);
    RUN_TEST(test_TCurve_getPoint_TCurve);

    return UNITY_END();
}