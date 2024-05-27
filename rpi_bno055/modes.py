# section 3.3

from . import Mode

# config mode (section 3.3.1)
CONFIG = Mode(0b0000_0000)
# non-fusion mode (section 3.3.2)
ACCONLY = Mode(0b0000_0001)
MAGONLY = Mode(0b0000_0010)
GYROONLY = Mode(0b0000_0011)
ACCMAG = Mode(0b0000_0100)
ACCGYRO = Mode(0b0000_0101)
MAGGYRO = Mode(0b0000_0110)
AMG = Mode(0b0000_0111)
# fusion mode(section 3.3.3)
IMU = Mode(0b0000_1000)
COMPASS = Mode(0b0000_1001)
M4G = Mode(0b0000_1010)
NDOF_FMC_OFF = Mode(0b0000_1011)
NDOF = Mode(0b0000_1100)
