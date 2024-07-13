from typing import List

class App:
    APP_WIDTH: int = 900
    APP_HEIGHT: int = 800

class Robot:
    LENGTHS: tuple = \
        (
            100.0, #l1
            100.0, #l2
            100.0, #l3
            100.0, #l4
            50.0  #l5
        )
    INIT_END_POINT: List[float] = \
        [
            25,
            150
        ]

class Test:
    test: int = 100