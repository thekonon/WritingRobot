"""
TCurve trajectory generation library
"""
from __future__ import annotations
import typing
__all__: list[str] = ['TCurve', 'TCurveError', 'TCurveType']
class TCurve:
    def __init__(self) -> None:
        ...
    def get_acceleration(self) -> float:
        ...
    def get_curve_type(self) -> TCurveType:
        ...
    def get_delta_phi(self) -> float:
        ...
    def get_max_velocity(self) -> float:
        ...
    def get_point(self, time: float) -> tuple:
        ...
    def get_t1(self) -> float:
        ...
    def get_t2(self) -> float:
        ...
    def get_tmax(self) -> float:
        ...
    def get_wmax(self) -> float:
        ...
    def recalculate(self) -> TCurveError:
        ...
    def set_acceleration(self, acceleration: float) -> TCurveError:
        ...
    def set_delta_phi(self, delta_phi: float) -> TCurveError:
        ...
    def set_max_velocity(self, velocity: float) -> TCurveError:
        ...
class TCurveError:
    """
    Members:
    
      OK
    
      NotOk
    
      InvalidSetting
    
      MustBeNonZeroFinite
    
      TimeOutOfRange
    
      NotImplemented
    
      NotInitialized
    """
    InvalidSetting: typing.ClassVar[TCurveError]  # value = <TCurveError.InvalidSetting: 2>
    MustBeNonZeroFinite: typing.ClassVar[TCurveError]  # value = <TCurveError.MustBeNonZeroFinite: 3>
    NotImplemented: typing.ClassVar[TCurveError]  # value = <TCurveError.NotImplemented: 5>
    NotInitialized: typing.ClassVar[TCurveError]  # value = <TCurveError.NotInitialized: 6>
    NotOk: typing.ClassVar[TCurveError]  # value = <TCurveError.NotOk: 1>
    OK: typing.ClassVar[TCurveError]  # value = <TCurveError.OK: 0>
    TimeOutOfRange: typing.ClassVar[TCurveError]  # value = <TCurveError.TimeOutOfRange: 4>
    __members__: typing.ClassVar[dict[str, TCurveError]]  # value = {'OK': <TCurveError.OK: 0>, 'NotOk': <TCurveError.NotOk: 1>, 'InvalidSetting': <TCurveError.InvalidSetting: 2>, 'MustBeNonZeroFinite': <TCurveError.MustBeNonZeroFinite: 3>, 'TimeOutOfRange': <TCurveError.TimeOutOfRange: 4>, 'NotImplemented': <TCurveError.NotImplemented: 5>, 'NotInitialized': <TCurveError.NotInitialized: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class TCurveType:
    """
    Members:
    
      TCurve
    
      SCurve
    
      NotInitialized
    """
    NotInitialized: typing.ClassVar[TCurveType]  # value = <TCurveType.NotInitialized: 2>
    SCurve: typing.ClassVar[TCurveType]  # value = <TCurveType.SCurve: 1>
    TCurve: typing.ClassVar[TCurveType]  # value = <TCurveType.TCurve: 0>
    __members__: typing.ClassVar[dict[str, TCurveType]]  # value = {'TCurve': <TCurveType.TCurve: 0>, 'SCurve': <TCurveType.SCurve: 1>, 'NotInitialized': <TCurveType.NotInitialized: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
