# section 3.3

from typing import NewType

OperatingMode = NewType("OperatingMode", int)

# config mode (section 3.3.1)
CONFIG = OperatingMode(0b0000_0000)
# non-fusion mode (section 3.3.2)
ACCONLY = OperatingMode(0b0000_0001)
MAGONLY = OperatingMode(0b0000_0010)
GYROONLY = OperatingMode(0b0000_0011)
ACCMAG = OperatingMode(0b0000_0100)
ACCGYRO = OperatingMode(0b0000_0101)
MAGGYRO = OperatingMode(0b0000_0110)
AMG = OperatingMode(0b0000_0111)
# fusion mode(section 3.3.3)
IMU = OperatingMode(0b0000_1000)
COMPASS = OperatingMode(0b0000_1001)
M4G = OperatingMode(0b0000_1010)
NDOF_FMC_OFF = OperatingMode(0b0000_1011)
NDOF = OperatingMode(0b0000_1100)
