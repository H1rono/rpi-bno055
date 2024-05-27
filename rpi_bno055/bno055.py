import smbus2

from . import RegisterAddress


class BNO055:
    from . import constants, regaddrs0

    def __init__(self, bno055_address: int = constants.DEFAULT_ADDRESS, bus: smbus2.SMBus | None = None):
        self._i2c = bus or smbus2.SMBus(self.__class__.constants.DEFAULT_I2C_PORT)
        self._address = bno055_address

    def write_byte(self, register: RegisterAddress, value: int) -> None:
        self._i2c.write_byte_data(self._address, register, value)

    def read_byte(self, register: RegisterAddress) -> int:
        return self._i2c.read_byte_data(self._address, register)

    def read_block(self, register: RegisterAddress, length: int) -> list[int]:
        return self._i2c.read_i2c_block_data(self._address, register, length)

    def write_mode(self, mode: int) -> None:
        self.write_byte(BNO055.regaddrs0.OPR_MODE, mode)

    def read_mode(self) -> int:
        return self.read_byte(BNO055.regaddrs0.OPR_MODE)

    def begin(self) -> None:
        assert self.read_byte(BNO055.regaddrs0.CHIP_ID) == 0xA0
        self.write_mode(0x00)
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
    def read_calibration_status(self) -> tuple[int, int, int, int]:
        buf = self.read_byte(BNO055.regaddrs0.CALIB_STAT)
        mag = (buf >> 0) & 0b11
        acc = (buf >> 2) & 0b11
        gyr = (buf >> 4) & 0b11
        sys = (buf >> 6) & 0b11
        return (mag, acc, gyr, sys)

    def read_system_status_code(self) -> int:
        return self.read_byte(BNO055.regaddrs0.SYS_STATUS)

    def read_system_error_code(self) -> int:
        return self.read_byte(BNO055.regaddrs0.SYS_ERR)

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


# bno055_addr: 0x28 or 0x29
def main(bno055_addr: int = 0x28, bus_port: str | int = "/dev/i2c-1") -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    print("begin success!")


if __name__ == "__main__":
    main()
