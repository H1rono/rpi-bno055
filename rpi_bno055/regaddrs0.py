# register addresses of Page 0
# section 4.2.1, Table 4-2

from typing import NewType


RegisterAddress = NewType("RegisterAddress", int)

MAG_RADIUS_MSB = RegisterAddress(0x6A)
MAG_RADIUS_LSB = RegisterAddress(0x69)
ACC_RADIUS_MSB = RegisterAddress(0x68)
ACC_RADIUS_LSB = RegisterAddress(0x67)
GYR_OFFSET_Z_MSB = RegisterAddress(0x66)
GYR_OFFSET_Z_LSB = RegisterAddress(0x65)
GYR_OFFSET_Y_MSB = RegisterAddress(0x64)
GYR_OFFSET_Y_LSB = RegisterAddress(0x63)
GYR_OFFSET_X_MSB = RegisterAddress(0x62)
GYR_OFFSET_X_LSB = RegisterAddress(0x61)
MAG_OFFSET_Z_MSB = RegisterAddress(0x60)
MAG_OFFSET_Z_LSB = RegisterAddress(0x5F)
MAG_OFFSET_Y_MSB = RegisterAddress(0x5E)
MAG_OFFSET_Y_LSB = RegisterAddress(0x5D)
MAG_OFFSET_X_MSB = RegisterAddress(0x5C)
MAG_OFFSET_X_LSB = RegisterAddress(0x5B)
ACC_OFFSET_Z_MSB = RegisterAddress(0x5A)
ACC_OFFSET_Z_LSB = RegisterAddress(0x59)
ACC_OFFSET_Y_MSB = RegisterAddress(0x58)
ACC_OFFSET_Y_LSB = RegisterAddress(0x57)
ACC_OFFSET_X_MSB = RegisterAddress(0x56)
ACC_OFFSET_X_LSB = RegisterAddress(0x55)
AXIS_MAP_SIGN = RegisterAddress(0x42)
AXIS_MAP_CONFIG = RegisterAddress(0x41)
TEMP_SOURCE = RegisterAddress(0x40)
SYS_TRIGGER = RegisterAddress(0x3F)
PWR_MODE = RegisterAddress(0x3E)
OPR_MODE = RegisterAddress(0x3D)
UNIT_SEL = RegisterAddress(0x3B)
SYS_ERR = RegisterAddress(0x3A)
SYS_STATUS = RegisterAddress(0x39)
SYS_CLK_STATUS = RegisterAddress(0x38)
INT_STA = RegisterAddress(0x37)
ST_RESULT = RegisterAddress(0x36)
CALIB_STAT = RegisterAddress(0x35)
TEMP = RegisterAddress(0x34)
GRV_DATA_Z_MSB = RegisterAddress(0x33)
GRV_DATA_Z_LSB = RegisterAddress(0x32)
GRV_DATA_Y_MSB = RegisterAddress(0x31)
GRV_DATA_Y_LSB = RegisterAddress(0x30)
GRV_DATA_X_MSB = RegisterAddress(0x2F)
GRV_DATA_X_LSB = RegisterAddress(0x2E)
LIA_DATA_Z_MSB = RegisterAddress(0x2D)
LIA_DATA_Z_LSB = RegisterAddress(0x2C)
LIA_DATA_Y_MSB = RegisterAddress(0x2B)
LIA_DATA_Y_LSB = RegisterAddress(0x2A)
LIA_DATA_X_MSB = RegisterAddress(0x29)
LIA_DATA_X_LSB = RegisterAddress(0x28)
QUA_DATA_Z_MSB = RegisterAddress(0x27)
QUA_DATA_Z_LSB = RegisterAddress(0x26)
QUA_DATA_Y_MSB = RegisterAddress(0x25)
QUA_DATA_Y_LSB = RegisterAddress(0x24)
QUA_DATA_X_MSB = RegisterAddress(0x23)
QUA_DATA_X_LSB = RegisterAddress(0x22)
QUA_DATA_W_MSB = RegisterAddress(0x21)
QUA_DATA_W_LSB = RegisterAddress(0x20)
EUL_PITCH_MSB = RegisterAddress(0x1F)
EUL_PITCH_LSB = RegisterAddress(0x1E)
EUL_ROLL_MSB = RegisterAddress(0x1D)
EUL_ROLL_LSB = RegisterAddress(0x1C)
EUL_HEADING_MSB = RegisterAddress(0x1B)
EUL_HEADING_LSB = RegisterAddress(0x1A)
GYR_DATA_Z_MSB = RegisterAddress(0x19)
GYR_DATA_Z_LSB = RegisterAddress(0x18)
GYR_DATA_Y_MSB = RegisterAddress(0x17)
GYR_DATA_Y_LSB = RegisterAddress(0x16)
GYR_DATA_X_MSB = RegisterAddress(0x15)
GYR_DATA_X_LSB = RegisterAddress(0x14)
MAG_DATA_Z_MSB = RegisterAddress(0x13)
MAG_DATA_Z_LSB = RegisterAddress(0x12)
MAG_DATA_Y_MSB = RegisterAddress(0x11)
MAG_DATA_Y_LSB = RegisterAddress(0x10)
MAG_DATA_X_MSB = RegisterAddress(0x0F)
MAG_DATA_X_LSB = RegisterAddress(0x0E)
ACC_DATA_Z_MSB = RegisterAddress(0x0D)
ACC_DATA_Z_LSB = RegisterAddress(0x0C)
ACC_DATA_Y_MSB = RegisterAddress(0x0B)
ACC_DATA_Y_LSB = RegisterAddress(0x0A)
# Upper byte of X axis Acceleration data, read-only
# The output units can be selected using the `UNIT_SEL` register and data output type can be changed
# by updating the Operation Mode in the `OPR_MODE` register, see section 3.3
ACC_DATA_X_MSB = RegisterAddress(0x09)
# Lower byte of X axis Acceleration data, read-only
# The output units can be selected using the `UNIT_SEL` register and data output type can be changed
# by updating the Operation Mode in the `OPR_MODE` register, see section 3.3
ACC_DATA_X_LSB = RegisterAddress(0x08)
# Read: Number of currently selected page
# Write: Change page, 0x00, 0x01
PAGE_ID = RegisterAddress(0x07)
# Identifies the version of the bootloader in the microcontroller, read-only
BL_REV_ID = RegisterAddress(0x06)
# Upper byte of SW Revision ID, read-only fixed value depending on SW revision programmed on microcontroller
SW_REV_ID_MSB = RegisterAddress(0x05)
# Lower byte of SW Revision ID, read-only fixed value depending on SW revision programmed on microcontroller
SW_REV_ID_LSB = RegisterAddress(0x04)
# Chip ID of the Gyroscope device, read-only fixed value `0x0F`
GYR_ID = RegisterAddress(0x03)
# Chip ID of the Magnetometer device, read0only fixed value `0x32`
MAG_ID = RegisterAddress(0x02)
# Chip ID of the Accelerometer device, read-only fixed value `0xFB`
ACC_ID = RegisterAddress(0x01)
# Chip identification code, read-only fixed value `0xA0`
CHIP_ID = RegisterAddress(0x00)
