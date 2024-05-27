from typing import NewType

from .bno055 import BNO055
from .constants import SysTriggerFlag


RegisterAddress = NewType("RegisterAddress", int)
OperatingMode = NewType("OperatingMode", int)
SysStatusCode = NewType("SysStatusCode", int)
SysErrCode = NewType("SysErrCode", int)
PowerMode = NewType("PowerMode", int)

__all__ = ["BNO055", "SysTriggerFlag"]
