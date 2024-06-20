#include <Arduino.h>
#include <motor_control.h>
#include <SPI.h>
#include <mcp2515.h>
#include <constants.h>

// CAN communication
struct can_frame can_MSG1;
MCP2515 mcp2515(MPC_CS_PIN);

// Internal function prototypes
void set_up_mpc2515();
void set_up_pin_modes();
void read_can_msg_values(
  float *wanted_val_1,
  float *wanted_val_2
);
void update_needed_steps(
  float wanted_motor_angle,
  int current_step
);

void setup() {
  // Set up communication - debug only
  Serial.begin(115200);

  // Set up CAN communication
  set_up_mpc2515();

  // Set up pins to correct pin mode
  set_up_pin_modes();
}

void loop() {
  // Wanted angles of motors
  float wanted_angle_1;     // Value transfered via CAN
  float wanted_angle_2;     // Value transfered via CAN

  int steps_needed_1;       // Stepps that has to be send in order to achive wanted angle
  int steps_needed_2;       // Stepps that has to be send in order to achive wanted angle


  // Do something when you get a normal can msg
  if(mcp2515.readMessage(&can_MSG1) == MPC2515::ERROR_OK)
  {
    // Update wanted values
    read_can_msg_values(&wanted_angle_1, &wanted_angle_2);
  }
}

void set_up_mpc2515()
{
  /*
    Set up the properties of the MCP2515 controller
  */
  mcp2515.reset();
  mcp2515.setBitrate(MPC_BITRATE, MPC_CLOCK);
  mcp2515.setNormalMode();
}

void set_up_pin_modes()
{
  /*
    Set up the pin modes of arduino PINS
  */
  pinMode(STEP_PIN_MOTOR_1, OUTPUT);
  pinMode(STEP_PIN_MOTOR_2, OUTPUT);
  pinMode(DIR_PIN_MOTOR_1, OUTPUT);
  pinMode(DIR_PIN_MOTOR_2, OUTPUT);
}

void read_can_msg_values(float *wanted_angle_1, float *wanted_angle_2)
{
  /*
    Update the wanted motor angles from can msg
  */
 // TODO: add the decimal point numbers
 *wanted_angle_1 = can_MSG1.data[0]*255+can_MSG1.data[1];
 *wanted_angle_2 = can_MSG1.data[4]*255+can_MSG1.data[5];
}

void update_needed_steps(
  float wanted_motor_angle,
  int current_step
)