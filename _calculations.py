class Calculations:
    _FROM_MIN_VALUE = 0
    _FROM_MAX_VALUE = 990
    _MIN_VALUE = -360
    _MAX_VALUE = 360
    
    @classmethod
    def map_to_data(cls, value):
        mapped_value = cls.map_value(value)
        return cls.value_to_hex(mapped_value)
        
    
    @classmethod
    def map_value(cls, value: int):
        return cls._map_value(value,
                              cls._FROM_MIN_VALUE,
                              cls._FROM_MAX_VALUE,
                              cls._MIN_VALUE, 
                              cls._MAX_VALUE)
    
    @staticmethod
    def _map_value(value, from_min, from_max, to_min, to_max):
        if from_max < from_min:
            raise ValueError("Max must be bigger - from")
        if to_max < to_min:
            raise ValueError("Max must be bigger - to")
        
        procent = value / (from_max - from_min)
        return to_min + procent * (to_max - to_min)
    
    @staticmethod
    def value_to_hex(value: int):
        # 1st byte      - sign 0 - +
        # 2nd/3rd byte  - value before decimal
        # 4th byte      - after decimal value
        # e.g. 347.36 -> [0, 1, 91, 36]
        before_decimal = abs(int(value))
        after_decimal = int(abs(value) % 1 * 100)  # Extracting the first two decimal digits
        if before_decimal > 2 ** 16:
            raise ValueError("Too large number to be sent")
        if after_decimal > 2 ** 8:
            raise ValueError("Too large number to be sent")
        hex_sign = "00" if value >= 0 else "01"  # Padding sign to 2 characters

        hex_before_decimal = format(before_decimal, '04x')  # Padding to 4 characters
        hex_after_decimal = format(after_decimal, '02x')  # Padding to 2 characters

        # Returning list of integers representing hex values
        return [int(hex_sign, 16), int(hex_before_decimal[:2], 16), int(hex_before_decimal[2:], 16), int(hex_after_decimal, 16)]
    
    
    