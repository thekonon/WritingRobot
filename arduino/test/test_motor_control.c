#include "unity.h"
#include "motor_control.h"

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

int main(void) {
    UNITY_BEGIN();
    RUN_TEST(test_moveStraight);
    RUN_TEST(test_moveArc);
    return UNITY_END();
}
