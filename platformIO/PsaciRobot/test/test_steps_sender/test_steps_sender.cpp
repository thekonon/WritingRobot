#include <Arduino.h>
#include <unity.h>
#include "steps_sender.h"
#include "constants.h"

// Mocks for hardware-specific functions and variables
uint8_t mockPORTD = 0;
void delay(int ms) { /* do nothing */ }
void delayMicroseconds(int us) { /* do nothing */ }

// Override the PORTD with the mock version
#define PORTD mockPORTD

void setUp(void) {
    // Set up before each test
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

void test_set_motor_2_dir_high(void) {
    set_motor_2_dir(true);
    TEST_ASSERT_EQUAL_UINT8(0, PORTD & (1 << DIR_PIN_MOTOR_2)); // Ensure the DIR_PIN_MOTOR_2 is HIGH
}

void test_set_motor_2_dir_low(void) {
    set_motor_2_dir(false);
    TEST_ASSERT_EQUAL_UINT8(1 << DIR_PIN_MOTOR_2, PORTD & (1 << DIR_PIN_MOTOR_2)); // Ensure the DIR_PIN_MOTOR_2 is LOW
}

void test_send_steps_motor_1_forward(void) {
    send_steps_motor_1(5);
    TEST_ASSERT_EQUAL(5, stepCounterA);
    TEST_ASSERT_EQUAL(0, stepCounterB);
}

void test_send_steps_motor_1_backward(void) {
    send_steps_motor_1(-5);
    TEST_ASSERT_EQUAL(0, stepCounterA);
    TEST_ASSERT_EQUAL(5, stepCounterB);
}

void test_send_steps_motor_2_forward(void) {
    send_steps_motor_2(5);
    TEST_ASSERT_EQUAL(5, stepCounterA);
    TEST_ASSERT_EQUAL(0, stepCounterB);
}

void test_send_steps_motor_2_backward(void) {
    send_steps_motor_2(-5);
    TEST_ASSERT_EQUAL(0, stepCounterA);
    TEST_ASSERT_EQUAL(5, stepCounterB);
}

void test_one_step_motor_1_forward(void) {
    one_step_motor_1(true);
    TEST_ASSERT_EQUAL(1, stepCounterA);
    TEST_ASSERT_EQUAL(0, stepCounterB);
}

void test_one_step_motor_1_backward(void) {
    one_step_motor_1(false);
    TEST_ASSERT_EQUAL(0, stepCounterA);
    TEST_ASSERT_EQUAL(1, stepCounterB);
}

void test_one_step_motor_2_forward(void) {
    one_step_motor_2(true);
    TEST_ASSERT_EQUAL(1, stepCounterA);
    TEST_ASSERT_EQUAL(0, stepCounterB);
}

void test_one_step_motor_2_backward(void) {
    one_step_motor_2(false);
    TEST_ASSERT_EQUAL(0, stepCounterA);
    TEST_ASSERT_EQUAL(1, stepCounterB);
}

int main(int argc, char **argv) {
    UNITY_BEGIN();
    RUN_TEST(test_set_motor_1_dir_high);
    RUN_TEST(test_set_motor_1_dir_low);
    // RUN_TEST(test_set_motor_2_dir_high);
    // RUN_TEST(test_set_motor_2_dir_low);
    // RUN_TEST(test_send_steps_motor_1_forward);
    // RUN_TEST(test_send_steps_motor_1_backward);
    // RUN_TEST(test_send_steps_motor_2_forward);
    // RUN_TEST(test_send_steps_motor_2_backward);
    // RUN_TEST(test_one_step_motor_1_forward);
    // RUN_TEST(test_one_step_motor_1_backward);
    // RUN_TEST(test_one_step_motor_2_forward);
    // RUN_TEST(test_one_step_motor_2_backward);
    UNITY_END();
    return 0;
}
