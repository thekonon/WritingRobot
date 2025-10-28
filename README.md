
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

![Arduino](01_Doc/Img/Electrical/BluePill.png)

Stepper motors

![Stepper1](01_Doc/Img/Electrical/Stepper_1.png)
![Stepper2](01_Doc/Img/Electrical/Stepper_2.png)

Powerline

![POWERLINE](01_Doc/Img/Electrical/Power.png)

MCP2551 CANH/L -> Rx/Tx data module

![MCP2551](01_Doc/Img/Electrical/MCP2551.png)

L7805 -> 12V -> 5V/1A 

![L7805](01_Doc/Img/Electrical/L7805.png)

## Board design

Wiring scheme of actual PCB

![BoardScheme](01_Doc/Img/Board/Board_scheme.png)

3D view to the board without and with modules

![BoardWithoutComponents](01_Doc/Img/Board/Board_3d_without_components.png)
![BoardWithComponents](01_Doc/Img/Board/Board_3d_with_components.png)
