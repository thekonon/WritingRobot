from typing import List
from dataclasses import dataclass

@dataclass
class Signal:
    msg_name: str = ""
    signal_name: str = ""
    ID: int = 0
    unit: str = ""
    length: int = 0
    start_bit: int = 0
    value_range: int = 0
    init_value: int = 0
    source: str = ""
    description: str = ""

class KMatrix:
    def __init__(self):
        self.KMatrix_path: str = "src/datamatrix/MotorCAN.csv"
        self.KMatrix_export: str = "src/datamatrix/data.c"
        self.signals: List[Signal] = []
        self.process_data()

    def load_data(self):
        with open(self.KMatrix_path) as file:
            return list(file)
        
    def process_data(self):
        self.data = self.load_data()
        for line in self.data[1:]:  # Skip the header
            split = line.strip().split(",")
            if len(split) == 10:  # Ensure there are exactly 10 columns
                signal = Signal(
                    msg_name=split[0],
                    signal_name=split[1],
                    ID=int(split[2]),
                    unit=split[3],
                    length=int(split[4]),  # Length in bits
                    start_bit=int(split[5]),
                    value_range=int(split[6]),
                    init_value=int(split[7]),
                    source=split[8],
                    description=split[9]
                )
                self.signals.append(signal)

    def export_data(self):
        with open(self.KMatrix_export, "w") as file:
            # Write the struct definition
            file.write(
                "struct Config {\n"
                "    char category[20];  // Example: \"Config_steps\"\n"
                "    char name[20];      // Example: \"Microstepping_M1\"\n"
                "    uint8_t id;         // Example: 100\n"
                "    char unit[5];       // Example: \"/\"\n"
                "    uint8_t length;     // Example: 3\n"
                "    uint8_t offset;     // Example: 0\n"
                "    uint16_t max_value; // Example: 8\n"
                "    uint16_t value;     // Example: 8\n"
                "    char source[10];    // Example: \"MCU\"\n"
                "};\n\n"
            )

            # Write the header of the C array
            file.write("Config config_table[] = {\n")
            
            # Iterate over signals and write each entry
            for signal in self.signals:
                file.write(f'    {{"{signal.msg_name}", "{signal.signal_name}", {signal.ID}, "{signal.unit}", '
                           f'{signal.length}, {signal.start_bit}, {signal.value_range}, {signal.init_value}, '
                           f'"{signal.source}"}},\n')

            # Close the array declaration
            file.write("};\n")

# Example usage
matrix = KMatrix()
matrix.export_data()
