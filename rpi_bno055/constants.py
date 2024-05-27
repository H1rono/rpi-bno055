from enum import IntFlag as _IntFlag


DEFAULT_ADDRESS = 0x28
ALT_ADDRESS = 0x29
DEFAULT_I2C_PORT = "/dev/i2c-1"
# section 4.3.1
BNO055_CHIP_ID = 0xA0


# section 4.3.63
class SysTriggerFlag(_IntFlag):
    # 0: Use internal oscillator
    # 1: Use external oscillator. Set this bit only if external crystal is connected
    CLK_SEL = 0b1000_0000
    # Set to reset all interrupt status bits, and INT output
    RST_INT = 0b0100_0000
    # Set to reset system
    RST_SYS = 0b0010_0000
    # Set to trigger selftest
    SELFTEST = 0b0000_0001
    # normal state
    NO_TRIGGER = 0b0000_0000
