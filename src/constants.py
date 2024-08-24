from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class appSettings:
    APP_WIDTH: int = 900
    APP_HEIGHT: int = 800

@dataclass
class robotSettings:
    LENGTHS: tuple = \
        (
            100.0, #l1
            100.0, #l2
            100.0, #l3
            100.0, #l4
            50.0  #l5
        )
    INIT_END_POINT: Tuple[float, float] = \
        (
            25,
            150
        )


