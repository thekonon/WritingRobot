from typing import List
class Calculations:
    _FROM_MIN_VALUE: int = 0
    _FROM_MAX_VALUE: int = 360
    _MIN_VALUE: int = 0
    _MAX_VALUE: int = 360

    @classmethod
    def map_to_data(cls, value):
        mapped_value = cls.map_value(value)
        return cls.value_to_hex_2(mapped_value)

    @classmethod
    def map_value(cls, value: int):
        return cls._map_value(
            value,
            cls._FROM_MIN_VALUE,
            cls._FROM_MAX_VALUE,
            cls._MIN_VALUE,
            cls._MAX_VALUE,
        )

    @staticmethod
    def _map_value(value, from_min, from_max, to_min, to_max):
        if from_max < from_min:
            raise ValueError("Max must be bigger - from")
        if to_max < to_min:
            raise ValueError("Max must be bigger - to")

        procent = value / (from_max - from_min)
        return to_min + procent * (to_max - to_min)

    @staticmethod
    def value_to_hex(value: float):
        # 1st byte      - sign 0 - +
        # 2nd/3rd byte  - value before decimal
        # 4th byte      - after decimal value
        # e.g. 347.36 -> [0, 1, 91, 36]
        before_decimal = abs(int(value))
        after_decimal = int(
            abs(value) % 1 * 100
        )  # Extracting the first two decimal digits
        if before_decimal > 2**16:
            raise ValueError("Too large number to be sent")
        if after_decimal > 2**8:
            raise ValueError("Too large number to be sent")
        hex_sign = "00" if value >= 0 else "01"  # Padding sign to 2 characters

        hex_before_decimal = format(before_decimal, "04x")  # Padding to 4 characters
        hex_after_decimal = format(after_decimal, "02x")  # Padding to 2 characters

        # Returning list of integers representing hex values
        return [
            int(hex_sign, 16),
            int(hex_before_decimal[:2], 16),
            int(hex_before_decimal[2:], 16),
            int(hex_after_decimal, 16),
        ]
    @staticmethod
    def value_to_hex_2(value: float) -> List[int]:
        """New function to convert a motor rotation to can MSG
            Solution to this ticket:
            https://github.com/thekonon/WritingRobot/issues/7

        Args:
            value (float): Wanted motor rotation

        Returns:
            List[int]: List of ints representing half of the CAN frame
            
        E.G:
        312.1234564 -> 312 and 1234567
        keeps only 4 decimal digits -> 123457 -> 1234
        312     -> 0x0138 -> 01 38
        1234    -> 0x04d2 -> 04 d2
        final output is [01, 38, 04, d2]
        """
        # Apply modulo 360 to keep the number within range 0-360
        value = value % 360
        print(f"Value of motor: {value}")

        # Split into whole and decimal parts
        whole_part = int(value)
        # Rounding the decimal part
        decimal_part = int((value - whole_part + 1e-7) * 10000)

        hex_before_decimal = format(whole_part, "04x")  # Padding to 4 characters
        hex_after_decimal = format(decimal_part, "04x")  # Padding to 2 characters
        return [
            int(hex_before_decimal[:2], 16),
            int(hex_before_decimal[2:], 16),
            int(hex_after_decimal[:2], 16),
            int(hex_after_decimal[2:], 16)
        ]