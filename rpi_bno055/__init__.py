from typing import NewType

from .constants import SysTriggerFlag


RegisterAddress = NewType("RegisterAddress", int)
Mode = NewType("Mode", int)
SysStatusCode = NewType("SysStatusCode", int)
SysErrCode = NewType("SysErrCode", int)
