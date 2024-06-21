#include <unity.h>
#include "steps_sender.h"
#include "MockArduino.h"

void setUp(void) {
    stepCounterA = 0;
    stepCounterB = 0;
    mockPORTD = 0;
}

void tearDown(void) {
    // Clean up after each test
}

void test_set_motor_1_dir_high(void) {
    set_motor_1_dir(true);
    TEST_ASSERT_EQUAL_UINT8(0, PORTD & (1 << DIR_PIN_MOTOR_1)); // Ensure the DIR_PIN_MOTOR_1 is HIGH
}

void test_set_motor_1_dir_low(void) {
    set_motor_1_dir(false);
    TEST_ASSERT_EQUAL_UINT8(1 << DIR_PIN_MOTOR_1, PORTD & (1 << DIR_PIN_MOTOR_1)); // Ensure the DIR_PIN_MOTOR_1 is LOW
}

// Additional test cases...

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_set_motor_1_dir_high);
    RUN_TEST(test_set_motor_1_dir_low);
    // Add additional tests
    UNITY_END();
    return 0;
}
