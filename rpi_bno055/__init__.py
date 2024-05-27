from typing import NewType

from .constants import SysTriggerFlag


RegisterAddress = NewType("RegisterAddress", int)
OperatingMode = NewType("OperatingMode", int)
SysStatusCode = NewType("SysStatusCode", int)
SysErrCode = NewType("SysErrCode", int)
PowerMode = NewType("PowerMode", int)
