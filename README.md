
# WritingRobot
Draw anything using robot!

## Overview

Robot is made of:
- Control part that runs on __Raspberry PI4__
- CAN communication using __MPC2515__ modules
- __Arduino__ Nano clone
- Two __stepper motors drivers__

# Schemes

## Electrical wiring

Arduino:

![Arduino](Docu/Img/Electrical/Arduino.png)

Stepper motors

![Stepper1](Docu/Img/Electrical/Stepper_1.png)
![Stepper2](Docu/Img/Electrical/Stepper_2.png)

Connection to CAN MCP2515 module

![MCP2515](Docu/Img/Electrical/MCP2515.png)

Powerline

![POWERLINE](Docu/Img/Electrical/Power.png)

## Board design

Wiring scheme of actual PCB

![BoardScheme](Docu/Img/Board/Board_scheme.png)

3D view to the board without and with modules

![BoardWithoutComponents](Docu/Img/Board/Board_3d_without_components.png)
![BoardWithComponents](Docu/Img/Board/Board_3d_with_components.png)