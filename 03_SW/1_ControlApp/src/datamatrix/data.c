struct Config {
    char category[20];  // Example: "Config_steps"
    char name[20];      // Example: "Microstepping_M1"
    uint8_t id;         // Example: 100
    char unit[5];       // Example: "/"
    uint8_t length;     // Example: 3
    uint8_t offset;     // Example: 0
    uint16_t max_value; // Example: 8
    uint16_t value;     // Example: 8
    char source[10];    // Example: "MCU"
};

Config config_table[] = {
    {"Config_steps", "Microstepping_M1", 100, "/", 3, 0, 8, 8, "MCU"},
    {"Config_steps", "Microstepping_M2", 100, "/", 3, 3, 8, 8, "MCU"},
    {"Config_cur_step", "Motor_1_cur_step", 101, "/", 14, 0, 16384, 0, "MCU"},
    {"Config_cur_step", "Motor_2_cur_step", 101, "/", 14, 14, 16384, 0, "MCU"},
    {"Config_lengths", "Length_1", 102, "mm", 12, 0, 4096, 100, "MCU"},
    {"Config_lengths", "Length_2", 102, "mm", 12, 12, 4096, 100, "MCU"},
    {"Config_lengths", "Length_3", 102, "mm", 12, 24, 4096, 100, "MCU"},
    {"Config_lengths", "Length_4", 102, "mm", 12, 36, 4096, 100, "MCU"},
    {"Config_lengths", "Length_5", 102, "mm", 12, 48, 4096, 50, "MCU"},
    {"Config_firmware", "Major", 103, "/", 8, 0, 255, 0, "MCU"},
    {"Config_firmware", "Minor", 103, "/", 8, 8, 255, 0, "MCU"},
    {"Req_mcu", "Microsteps", 50, "/", 1, 0, 2, 0, "*"},
    {"Req_mcu", "Cur_steps", 50, "/", 1, 1, 2, 0, "*"},
    {"Req_mcu", "Lengths", 50, "/", 1, 2, 2, 0, "*"},
    {"Req_mcu", "Firmware", 50, "/", 1, 3, 2, 0, "*"},
    {"Set_motors", "Motor_1", 10, "/", 14, 0, 16384, 0, "Controller"},
    {"Set_motors", "Motor_2", 10, "/", 14, 14, 16384, 0, "Controller"},
    {"Set_stepps", "Motor_1", 15, "/", 65, 0, 16384, 0, "Controller"},
};
