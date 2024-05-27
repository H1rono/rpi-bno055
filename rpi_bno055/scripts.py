import smbus2

from . import constants
from .bno055 import BNO055


# bno055_addr: 0x28 or 0x29
def begin(bno055_addr: int = constants.DEFAULT_ADDRESS, bus_port: str | int = constants.DEFAULT_I2C_PORT) -> None:
    bno055 = BNO055(bno055_addr, smbus2.SMBus(bus_port))
    bno055.begin()
    print("begin success!")


if __name__ == "__main__":
    begin()
