################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../Core/Startup/startup_stm32f103c6tx.s 

S_DEPS += \
./Core/Startup/startup_stm32f103c6tx.d 

OBJS += \
./Core/Startup/startup_stm32f103c6tx.o 


# Each subdirectory must supply rules for building sources it contributes
Core/Startup/%.o: ../Core/Startup/%.s Core/Startup/subdir.mk
	arm-none-eabi-gcc -mcpu=cortex-m3 -g3 -DDEBUG -c -I"C:/BigProjects/WritingRobot/03_SW/2_Firmware/lib/TCurve/inc" -I"C:/BigProjects/WritingRobot/03_SW/2_Firmware/lib/TCurve/src" -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@" "$<"

clean: clean-Core-2f-Startup

clean-Core-2f-Startup:
	-$(RM) ./Core/Startup/startup_stm32f103c6tx.d ./Core/Startup/startup_stm32f103c6tx.o

.PHONY: clean-Core-2f-Startup

