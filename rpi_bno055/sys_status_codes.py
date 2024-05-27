from typing import NewType


SysStatusCode = NewType("SysStatusCode", int)

# SYS_STATUS values
# section 4.3.58
SYSTEM_IDLE = SysStatusCode(0x00)
SYSTEM_ERROR = SysStatusCode(0x01)
PERIPHERALS_INIT = SysStatusCode(0x02)
SYSTEM_INIT = SysStatusCode(0x03)
EXEC_SELFTEST = SysStatusCode(0x04)
FUSION_ALGORITHM_RUNNING = SysStatusCode(0x05)
NO_FUSION_ALGORITHM_RUNNING = SysStatusCode(0x06)
