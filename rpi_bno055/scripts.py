import smbus2

from . import SysErrCode, constants, sys_err_codes as sys_err, sys_status_codes as sys_status
from .bno055 import BNO055


# bno055_addr: 0x28 or 0x29
def begin(bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT) -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    print("begin success!")


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
    error_str = "unknown"
    match error:
        case sys_err.NO_ERROR:
            error_str = "no error"
        case sys_err.PERIPHERAL_INIT_ERROR:
            error_str = "pheripheral initialization error"
        case sys_err.SYSTEM_INIT_ERROR:
            error_str = "system initialization error"
        case sys_err.SELF_TEST_FAILED:
            error_str = "selftest failed"
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


if __name__ == "__main__":
    begin()
