import smbus2

from .modes import OperatingMode
from .power_modes import PowerMode
from .regaddrs0 import RegisterAddress
from .sys_err_codes import SysErrCode
from .sys_status_codes import SysStatusCode


class BNO055:
    from . import constants, modes, power_modes, regaddrs0, sys_err_codes, sys_status_codes
    from .constants import SysTriggerFlag
    from .unit_sel import UnitSelection

    def __init__(self, bno055_address: int = constants.DEFAULT_ADDRESS, bus: smbus2.SMBus | None = None):
        self._i2c = bus or smbus2.SMBus(self.__class__.constants.DEFAULT_I2C_PORT)
        self._address = bno055_address

    def write_byte(self, register: RegisterAddress, value: int) -> None:
        self._i2c.write_byte_data(self._address, register, value)

    def read_byte(self, register: RegisterAddress) -> int:
        return self._i2c.read_byte_data(self._address, register)

    def read_block(self, register: RegisterAddress, length: int) -> list[int]:
        return self._i2c.read_i2c_block_data(self._address, register, length)

    def write_mode(self, mode: OperatingMode) -> None:
        self.write_byte(BNO055.regaddrs0.OPR_MODE, mode)

    def read_mode(self) -> OperatingMode:
        return OperatingMode(self.read_byte(BNO055.regaddrs0.OPR_MODE))

    def write_power_mode(self, mode: PowerMode) -> None:
        self.write_byte(BNO055.regaddrs0.PWR_MODE, mode)

    def read_power_mode(self) -> PowerMode:
        return PowerMode(self.read_byte(BNO055.regaddrs0.PWR_MODE))

    # section 3.8, 4.3.55
    # (Accelerometer, Magnetometer, Gyroscope, Microcontroller)
    # True: pass
    # False: fail
    def selftest_result(self) -> tuple[bool, bool, bool, bool]:
        buf = self.read_byte(BNO055.regaddrs0.ST_RESULT)
        acc = bool((buf >> 0) & 0b1)
        mag = bool((buf >> 1) & 0b1)
        gyr = bool((buf >> 2) & 0b1)
        mcu = bool((buf >> 3) & 0b1)
        return (acc, mag, gyr, mcu)

    def read_unit_selection(self) -> UnitSelection:
        buf = self.read_byte(BNO055.regaddrs0.UNIT_SEL)
        return BNO055.UnitSelection.from_value(buf)

    def write_unit_selection(self, unit_sel: UnitSelection) -> None:
        self.write_byte(BNO055.regaddrs0.UNIT_SEL, unit_sel.value)

    def update_unit_selection(self, val: UnitSelection.UnitsType) -> None:
        unit_sel = self.read_unit_selection()
        self.write_unit_selection(unit_sel.set(val))

    def begin(self) -> None:
        assert self.read_byte(BNO055.regaddrs0.CHIP_ID) == 0xA0
        self.write_mode(BNO055.modes.CONFIG)
        assert self.read_byte(BNO055.regaddrs0.CHIP_ID) == 0xA0

    # (SW_REV_ID_MSB, SW_REV_ID_LSB)
    def read_sw_revision_id(self) -> tuple[int, int]:
        buf = self.read_block(BNO055.regaddrs0.SW_REV_ID_LSB, 2)
        return (buf[0], buf[1])

    # (ACC_DATA_X, ACC_DATA_Y, ACC_DATA_Z)
    def read_raw_acc_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.ACC_DATA_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # (MAG_DATA_X, MAG_DATA_Y, MAG_DATA_Z)
    def read_raw_mag_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.MAG_DATA_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # (GYR_DATA_X, GYR_DATA_Y, GYR_DATA_Z)
    def read_raw_gyro_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.GYR_DATA_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # (EUL_HEADING, EUL_ROLL, EUL_PITCH)
    def read_raw_euler_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.EUL_HEADING_LSB, 6)
        heading = (buf[0] << 0) | (buf[1] << 8)
        roll = (buf[2] << 0) | (buf[3] << 8)
        pitch = (buf[4] << 0) | (buf[5] << 8)
        return (heading, roll, pitch)

    # (QUA_DATA_W, QUA_DATA_X, QUA_DATA_Y, QUA_DATA_Z)
    def read_raw_quaternion_data(self) -> tuple[int, int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.QUA_DATA_W_LSB, 6)
        w = (buf[0] << 0) | (buf[1] << 8)
        x = (buf[2] << 0) | (buf[3] << 8)
        y = (buf[4] << 0) | (buf[5] << 8)
        z = (buf[6] << 0) | (buf[7] << 8)
        return (w, x, y, z)

    # lia: linear acceleration
    # (LIA_DATA_X, LIA_DATA_Y, LIA_DATA_Z)
    def read_raw_lia_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.LIA_DATA_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # (GRV_DATA_X, GRV_DATA_Y, GRV_DATA_Z)
    def read_raw_gravity_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.GRV_DATA_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    def read_temperature(self) -> int:
        return self.read_byte(BNO055.regaddrs0.TEMP)

    # (mag, acc, gyr, sys)
    # 0 to 3; 3 indicates fully calibrated
    # section 3.10, 4.3.54
    def read_calibration_status(self) -> tuple[int, int, int, int]:
        buf = self.read_byte(BNO055.regaddrs0.CALIB_STAT)
        mag = (buf >> 0) & 0b11
        acc = (buf >> 2) & 0b11
        gyr = (buf >> 4) & 0b11
        sys = (buf >> 6) & 0b11
        return (mag, acc, gyr, sys)

    def read_system_status_code(self) -> SysStatusCode:
        return SysStatusCode(self.read_byte(BNO055.regaddrs0.SYS_STATUS))

    def read_system_error_code(self) -> SysErrCode:
        return SysErrCode(self.read_byte(BNO055.regaddrs0.SYS_ERR))

    # (ACC_OFFSET_X, ACC_OFFSET_Y, ACC_OFFSET_Z)
    def read_raw_acc_offset(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.ACC_OFFSET_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # (MAG_OFFSET_X, MAG_OFFSET_Y, MAG_OFFSET_Z)
    def read_raw_mag_offset(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.MAG_OFFSET_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # (GYR_OFFSET_X, GYR_OFFSET_Y, GYR_OFFSET_Z)
    def read_raw_gyr_offset(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.GYR_OFFSET_X_LSB, 6)
        x = (buf[0] << 0) | (buf[1] << 8)
        y = (buf[2] << 0) | (buf[3] << 8)
        z = (buf[4] << 0) | (buf[5] << 8)
        return (x, y, z)

    # ACC_RADIUS
    def read_raw_acc_radius(self) -> int:
        buf = self.read_block(BNO055.regaddrs0.ACC_RADIUS_LSB, 2)
        lsb = buf[0]
        msb = buf[1]
        return (lsb << 0) | (msb << 8)

    # MAG_RADIUS
    def read_raw_mag_radius(self) -> int:
        buf = self.read_block(BNO055.regaddrs0.MAG_RADIUS_LSB, 2)
        lsb = buf[0]
        msb = buf[1]
        return (lsb << 0) | (msb << 8)

    def system_trigger(self, trigger: SysTriggerFlag) -> None:
        from time import sleep
        self.write_byte(BNO055.regaddrs0.SYS_TRIGGER, trigger)
        # ensure triggering
        while True:
            try:
                id =  self.read_byte(BNO055.regaddrs0.CHIP_ID)
                if id == BNO055.constants.BNO055_CHIP_ID:
                    break
            except OSError:
                pass
            # for debug
            # print("BNO055.system_trigger: waiting...")
            sleep(0.05)
        self.write_byte(BNO055.regaddrs0.SYS_TRIGGER, BNO055.SysTriggerFlag.NO_TRIGGER)
