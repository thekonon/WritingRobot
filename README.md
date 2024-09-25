
# WritingRobot
Draw anything using robot!

## Overview

Robot is made of:
- Control part that runs on __Raspberry PI4__
- CAN communication using __MPC2515__ modules
- <del>__Arduino__ Nano clone</del>
- STM32 Bluepill (STM32F103C6T6
- Two __stepper motors drivers__

# Schemes

## Electrical wiring

Arduino:

![Arduino](docu/Img/Electrical/BluePill.png)

Stepper motors

![Stepper1](docu/Img/Electrical/Stepper_1.png)
![Stepper2](docu/Img/Electrical/Stepper_2.png)

Connection to CAN MCP2515 module

![MCP2515](docu/Img/Electrical/MCP2515.png)

Powerline

![POWERLINE](docu/Img/Electrical/Power.png)

MCP2551

![MCP2551](docu/Img/Electrical/MCP2551.png)

L7805

![L7805](docu/Img/Electrical/L7805.png)

## Board design

Wiring scheme of actual PCB

![BoardScheme](docu/Img/Board/Board_scheme.png)

3D view to the board without and with modules

![BoardWithoutComponents](docu/Img/Board/Board_3d_without_components.png)
![BoardWithComponents](docu/Img/Board/Board_3d_with_components.png)
