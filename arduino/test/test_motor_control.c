#include "unity.h"
#include "motor_control.h"
#include "constants.h"
#include "math.h"

void setUp(void) {
    // Set up before each test
}

void tearDown(void) {
    // Clean up after each test
}

void test_moveStraight(void) {
    moveStraight(30, 45, 2000, 2000);
    TEST_ASSERT_EQUAL(30, stepCounterA);
    TEST_ASSERT_EQUAL(45, stepCounterB);
}

void test_moveArc(void) {
    moveArc(30, 45, 2000, 2000);
    TEST_ASSERT_EQUAL(30, stepCounterA);
    TEST_ASSERT_EQUAL(45, stepCounterB);
}

void test_calculate_required_steps(void){
    int current_step = 0;
    float wanted_angle = 5;
    float ASC = STEP_ANGLE/MICRO_STEP;
    int result = calculate_required_steps(wanted_angle, current_step);
    TEST_ASSERT_EQUAL(round(wanted_angle/ASC), result);

    
    wanted_angle = 355;
    current_step = 0;
    result = calculate_required_steps(wanted_angle, current_step);
    TEST_ASSERT_EQUAL(-round((360-wanted_angle)/ASC), result);
    
    int wanted_step = 150;
    wanted_angle = wanted_step*ASC;
    current_step = 100;
    ASC = STEP_ANGLE/MICRO_STEP;
    result = calculate_required_steps(wanted_angle, current_step);
    TEST_ASSERT_EQUAL(50, result);

    wanted_step = 50;
    wanted_angle = wanted_step*ASC;
    current_step = 100;
    ASC = STEP_ANGLE/MICRO_STEP;
    result = calculate_required_steps(wanted_angle, current_step);
    TEST_ASSERT_EQUAL(-50, result);
    
}

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_moveStraight);
    RUN_TEST(test_moveArc);
    RUN_TEST(test_calculate_required_steps);
    return UNITY_END();
}
