from collections.abc import Sequence

import smbus2

from .modes import OperatingMode
from .power_modes import PowerMode
from .regaddrs0 import RegisterAddress
from .sys_err_codes import SysErrCode
from .sys_status_codes import SysStatusCode


def _bytes_to_i16s(seq: Sequence[int], length: int) -> list[int]:
    return [int.from_bytes(seq[i : i + 2], byteorder="little", signed=True) for i in range(0, length * 2, 2)]


class BNO055:
    from . import constants, modes, power_modes, regaddrs0, sys_err_codes, sys_status_codes
    from .constants import SysTriggerFlag
    from .unit_sel import UnitSelection

    def __init__(self, bno055_address: int = constants.DEFAULT_ADDRESS, bus: smbus2.SMBus | None = None):
        self._i2c = bus or smbus2.SMBus(self.__class__.constants.DEFAULT_I2C_PORT)
        self._address = bno055_address

    # section 4.6, figure 6
    def write_byte(self, register: RegisterAddress, value: int) -> None:
        self._i2c.write_byte_data(self._address, register, value)

    # section 4.6, figure 7
    def read_byte(self, register: RegisterAddress) -> int:
        return self._i2c.read_byte_data(self._address, register)

    # section 4.6, figure 7
    def read_block(self, register: RegisterAddress, length: int) -> list[int]:
        return self._i2c.read_i2c_block_data(self._address, register, length)

    # section 3.3, table 3-5
    def write_mode(self, mode: OperatingMode) -> None:
        self.write_byte(BNO055.regaddrs0.OPR_MODE, mode)

    # section 3.3, table 3-5
    def read_mode(self) -> OperatingMode:
        return OperatingMode(self.read_byte(BNO055.regaddrs0.OPR_MODE))

    # section 3.2, table 3-1
    def write_power_mode(self, mode: PowerMode) -> None:
        self.write_byte(BNO055.regaddrs0.PWR_MODE, mode)

    # section 3.2, table 3-1
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

    # section 3.6.1
    def read_unit_selection(self) -> UnitSelection:
        buf = self.read_byte(BNO055.regaddrs0.UNIT_SEL)
        return BNO055.UnitSelection.from_value(buf)

    # section 3.6.1
    def write_unit_selection(self, unit_sel: UnitSelection) -> None:
        self.write_byte(BNO055.regaddrs0.UNIT_SEL, unit_sel.value)

    # section 3.6.1
    def update_unit_selection(self, val: UnitSelection.UnitsType) -> None:
        unit_sel = self.read_unit_selection()
        self.write_unit_selection(unit_sel.set(val))

    def begin(self) -> None:
        assert self.read_byte(BNO055.regaddrs0.CHIP_ID) == 0xA0
        self.write_mode(BNO055.modes.CONFIG)
        assert self.read_byte(BNO055.regaddrs0.CHIP_ID) == 0xA0

    # (SW_REV_ID_MSB, SW_REV_ID_LSB)
    # section 4.2.1, 4.3.5, table 4-2
    # footnote 5, 6 at page 52
    def read_sw_revision_id(self) -> tuple[int, int]:
        buf = self.read_block(BNO055.regaddrs0.SW_REV_ID_LSB, 2)
        return (buf[0], buf[1])

    # (ACC_DATA_X, ACC_DATA_Y, ACC_DATA_Z)
    # section 3.6.5.1, table 3-25
    def read_raw_acc_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.ACC_DATA_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # (MAG_DATA_X, MAG_DATA_Y, MAG_DATA_Z)
    # section 3.6.5.2, table 3-26
    def read_raw_mag_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.MAG_DATA_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # (GYR_DATA_X, GYR_DATA_Y, GYR_DATA_Z)
    # section 3.6.5.3, table 3-27
    def read_raw_gyro_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.GYR_DATA_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # (EUL_HEADING, EUL_ROLL, EUL_PITCH)
    # section 3.6.5.4, table 3-28
    def read_raw_euler_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.EUL_HEADING_LSB, 6)
        heading, roll, pitch = _bytes_to_i16s(buf, 3)
        return (heading, roll, pitch)

    # (QUA_DATA_W, QUA_DATA_X, QUA_DATA_Y, QUA_DATA_Z)
    # section 3.6.5.5, table 3-30
    def read_raw_quaternion_data(self) -> tuple[int, int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.QUA_DATA_W_LSB, 6)
        w, x, y, z = _bytes_to_i16s(buf, 4)
        return (w, x, y, z)

    # lia: linear acceleration
    # (LIA_DATA_X, LIA_DATA_Y, LIA_DATA_Z)
    # section 3.6.5.6, table 3-32
    def read_raw_lia_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.LIA_DATA_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # (GRV_DATA_X, GRV_DATA_Y, GRV_DATA_Z)
    # section 3.6.5.7, table 3-34
    def read_raw_gravity_data(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.GRV_DATA_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # TEMP
    # section 3.6.5.8, table 3-36
    def read_raw_temperature_data(self) -> int:
        return int.from_bytes([self.read_byte(BNO055.regaddrs0.TEMP)], byteorder="big", signed=True)

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

    # section 4.3.58
    def read_system_status_code(self) -> SysStatusCode:
        return SysStatusCode(self.read_byte(BNO055.regaddrs0.SYS_STATUS))

    # section 4.3.59
    def read_system_error_code(self) -> SysErrCode:
        return SysErrCode(self.read_byte(BNO055.regaddrs0.SYS_ERR))

    # (ACC_OFFSET_X, ACC_OFFSET_Y, ACC_OFFSET_Z)
    # section 3.6.4.1, table 3-15
    def read_raw_acc_offset(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.ACC_OFFSET_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # (MAG_OFFSET_X, MAG_OFFSET_Y, MAG_OFFSET_Z)
    # section 3.6.4.2, table 3-18
    def read_raw_mag_offset(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.MAG_OFFSET_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # (GYR_OFFSET_X, GYR_OFFSET_Y, GYR_OFFSET_Z)
    # section 3.6.4.3, table 3-20
    def read_raw_gyr_offset(self) -> tuple[int, int, int]:
        buf = self.read_block(BNO055.regaddrs0.GYR_OFFSET_X_LSB, 6)
        x, y, z = _bytes_to_i16s(buf, 3)
        return (x, y, z)

    # ACC_RADIUS
    # section 3.6.4.4, table 3-24
    def read_raw_acc_radius(self) -> int:
        buf = self.read_block(BNO055.regaddrs0.ACC_RADIUS_LSB, 2)
        radius, *_ = _bytes_to_i16s(buf, 1)
        return radius

    # MAG_RADIUS
    def read_raw_mag_radius(self) -> int:
        buf = self.read_block(BNO055.regaddrs0.MAG_RADIUS_LSB, 2)
        radius, *_ = _bytes_to_i16s(buf, 1)
        return radius

    def system_trigger(self, trigger: SysTriggerFlag) -> None:
        from time import sleep

        self.write_byte(BNO055.regaddrs0.SYS_TRIGGER, trigger)
        # ensure triggering
        while True:
            try:
                id = self.read_byte(BNO055.regaddrs0.CHIP_ID)
                if id == BNO055.constants.BNO055_CHIP_ID:
                    break
            except OSError:
                pass
            # for debug
            # print("BNO055.system_trigger: waiting...")
            sleep(0.05)
        self.write_byte(BNO055.regaddrs0.SYS_TRIGGER, BNO055.SysTriggerFlag.NO_TRIGGER)

    # (acc_x, acc_y, acc_z)
    # section 3.6.4.1, table 3-17
    def read_accelerometer(self) -> tuple[float, float, float]:
        x, y, z = self.read_raw_acc_data()
        unit_sel = self.read_unit_selection()
        # 1 m/s^2 = 100 LSB, 1 mg = 1 LSB
        scale = 1 / 100.0 if unit_sel.acceleration == BNO055.UnitSelection.ACC_MPS2 else 1 / 1.0
        return (x * scale, y * scale, z * scale)

    # (mag_x, mag_y, mag_z)
    # section 3.6.4.2, table 3-19
    def read_magnetometer(self) -> tuple[float, float, float]:
        x, y, z = self.read_raw_mag_data()
        # 1 μT = 16 LSB
        scale = 1 / 16.0
        return (x * scale, y * scale, z * scale)

    # (gyro_x, gyro_y, gyro_z)
    # section 3.6.4.3, table 3-22
    def read_gyroscope(self) -> tuple[float, float, float]:
        x, y, z = self.read_raw_gyro_data()
        unit_sel = self.read_unit_selection()
        # 1 dps = 16 LSB, 1 rps = 900 LSB
        scale = 1 / 16.0 if unit_sel.gyroscope == BNO055.UnitSelection.GYR_DPS else 1 / 900.0
        return (x * scale, y * scale, z * scale)

    # (euler_heading, euler_roll, euler_pitch)
    # section 3.6.5.4, table 3-29
    def read_euler(self) -> tuple[float, float, float]:
        heading, roll, pitch = self.read_raw_euler_data()
        unit_sel = self.read_unit_selection()
        # 1 degrees = 16 LSB, 1 radian = 900 LSB
        scale = 1 / 16.0 if unit_sel.euler == BNO055.UnitSelection.EUL_DEGREES else 1 / 900.0
        return (heading * scale, roll * scale, pitch * scale)

    # (quat_w, quat_x, quat_y, quat_z)
    # section 3.6.5.5, table 3-31
    def read_quaternion(self) -> tuple[float, float, float, float]:
        w, x, y, z = self.read_raw_quaternion_data()
        # 1 [unit less] = 2^14 LSB
        scale = 1 / 0b0100_0000_0000_0000
        return (w * scale, x * scale, y * scale, z * scale)

    # (lia_x, lia_y, lia_z)
    # section 3.6.5.6, table 3-33
    def read_linear_accel(self) -> tuple[float, float, float]:
        x, y, z = self.read_raw_lia_data()
        unit_sel = self.read_unit_selection()
        # 1 m/s^2 = 100 LSB, 1 mg = 1 LSB
        scale = 1 / 100.0 if unit_sel.acceleration == BNO055.UnitSelection.ACC_MPS2 else 1 / 1.0
        return (x * scale, y * scale, z * scale)

    # (grav_x, grav_y, grav_z)
    # section 3.6.5.7, table 3-35
    def read_gravity(self) -> tuple[float, float, float]:
        x, y, z = self.read_raw_gravity_data()
        unit_sel = self.read_unit_selection()
        # 1 m/s^2 = 100 LSB, 1 mg = 1 LSB
        scale = 1 / 100.0 if unit_sel.acceleration == BNO055.UnitSelection.ACC_MPS2 else 1 / 1.0
        return (x * scale, y * scale, z * scale)

    # temperature
    # section 3.6.5.8, table 3-37
    def read_temperature(self) -> float:
        temp = self.read_raw_temperature_data()
        unit_sel = self.read_unit_selection()
        # 1 ℃ = 1 LSB, 2 F = 1 LSB
        scale = 1 / 1.0 if unit_sel.temperature == BNO055.UnitSelection.TEMP_CELSIUS else 2 / 1.0
        return temp * scale
