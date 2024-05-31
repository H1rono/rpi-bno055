from time import sleep

import smbus2

from . import constants, sys_err_codes as sys_err, sys_status_codes as sys_status
from .bno055 import BNO055
from .constants import SysTriggerFlag
from .sys_err_codes import SysErrCode


def begin(bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT) -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    print("begin success! triggering system reset...")
    bno055.system_trigger(SysTriggerFlag.RST_SYS)
    print("done!")


def system_status(
    bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT
) -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    status = bno055.read_system_status_code()
    status_str = "unknown"
    error: SysErrCode | None = None
    match status:
        case sys_status.SYSTEM_IDLE:
            status_str = "idle"
        case sys_status.SYSTEM_ERROR:
            status_str = "error"
            error = bno055.read_system_error_code()
        case sys_status.PERIPHERALS_INIT:
            status_str = "peripherals initializing"
        case sys_status.SYSTEM_INIT:
            status_str = "system initializing"
        case sys_status.EXEC_SELFTEST:
            status_str = "executing selftest"
        case sys_status.FUSION_ALGORITHM_RUNNING:
            status_str = "fusion algorithm running"
        case sys_status.NO_FUSION_ALGORITHM_RUNNING:
            status_str = "no-fusion algorithm running"
    if error is None:
        print(f"bno055 status: {status_str}; no-error")
        return
    error_str = "unknown"
    match error:
        case sys_err.NO_ERROR:
            error_str = "no error"
        case sys_err.PERIPHERAL_INIT_ERROR:
            error_str = "pheripheral initialization error"
        case sys_err.SYSTEM_INIT_ERROR:
            error_str = "system initialization error"
        case sys_err.SELF_TEST_FAILED:
            st_result = bno055.selftest_result()
            error_str = f"selftest failed with result: {st_result}"
        case sys_err.REGISTER_VALUE_OUT_OF_RANGE:
            error_str = "register value out of range"
        case sys_err.REGISTER_ADDRESS_OUT_OF_RANGE:
            error_str = "register address out of range"
        case sys_err.REGISTER_WRITE_ERROR:
            error_str = "register write error"
        case sys_err.LOW_POWER_MODE_UNAVAILABLE:
            error_str = "low power mode unavailable"
        case sys_err.ACCLEROMETER_POWER_MODE_UNAVAILABLE:
            error_str = "accelerometer power mode unavailable"
        case sys_err.FUSION_ALGORITHM_CONFGURATION_ERROR:
            error_str = "fusion algorithm configuration error"
        case sys_err.SENSOR_CONFIGURATION_ERROR:
            error_str = "sensor configuration error"
    print(f"bno055 is in error: {error_str}")


def calibration_check(
    bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT
) -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    print("connected to bno055. resetting system...")
    bno055.system_trigger(BNO055.SysTriggerFlag.RST_SYS)
    print("done. watching calibration status...")
    while True:
        mag, acc, gyr, sys = bno055.read_calibration_status()
        print(f"{mag=}, {acc=}, {gyr=}, {sys=}")
        if mag == acc == gyr == sys == 3:
            print("bno055 is fully calibrated!")
            break
        sleep(0.1)


def acconly(bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT) -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    bno055.system_trigger(BNO055.SysTriggerFlag.RST_SYS)
    status = bno055.read_system_status_code()
    if status == bno055.sys_status_codes.SYSTEM_ERROR:
        err = bno055.read_system_error_code()
        print(f"bno055 is in system error with code: {err}")
        return
    bno055.update_unit_selection(BNO055.UnitSelection.ACC_MPS2)
    bno055.write_mode(BNO055.modes.ACCONLY)
    while True:
        try:
            acc = bno055.read_accelerometer()
            print(f"accelerometer value: {acc}")
        except OSError:
            print("waiting bno055 getting ready...")
        sleep(1)


def imu(bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT) -> None:
    # In the IMU mode the relative orientation of the BNO055 in space is calculated
    # from the accelerometer and gyroscope data. The calculation is fast (i.e. high output data rate).
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    bno055.system_trigger(BNO055.SysTriggerFlag.RST_SYS)
    status = bno055.read_system_status_code()
    if status == bno055.sys_status_codes.SYSTEM_ERROR:
        err = bno055.read_system_error_code()
        print(f"bno055 is in system error with code: {err}")
        return
    # accelerometer: m/s^2
    bno055.update_unit_selection(BNO055.UnitSelection.ACC_MPS2)
    # gyroscope: rad/s
    bno055.update_unit_selection(BNO055.UnitSelection.GYR_RPS)
    # euler: radians
    bno055.update_unit_selection(BNO055.UnitSelection.EUL_RADIANS)
    bno055.write_mode(BNO055.modes.IMU)
    while True:
        try:
            accel = bno055.read_accelerometer()
            linear_accel = bno055.read_linear_accel()
            gravity = bno055.read_gravity()
            euler = bno055.read_euler()
            print(f"IMU data:\n{accel=} [m/s^2]\n{linear_accel=} [m/s^2]\n{gravity=} [m/s^2]\n{euler=} [rad]\n", end="")
        except OSError:
            print("waiting bno055 getting ready...")
        sleep(1)


if __name__ == "__main__":
    begin()
