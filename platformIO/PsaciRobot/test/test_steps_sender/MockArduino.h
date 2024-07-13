#ifndef MOCK_ARDUINO_H
#define MOCK_ARDUINO_H

#include <stdint.h>

// Mocking Arduino specific functions and variables
extern uint8_t mockPORTD;
#define PORTD mockPORTD

// Mocking delay functions
void delay(int ms);
void delayMicroseconds(int us);

#endif // MOCK_ARDUINO_H
