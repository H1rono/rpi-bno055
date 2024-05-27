import enum as _enum
from typing_extensions import Self


# section 3.6.2
class OrientationUnits(_enum.Enum):
    WINDOWS = 0
    ANDROID = 1

    @classmethod
    def default(cls) -> Self:
        return cls.WINDOWS # type: ignore


# section 3.6.1
class TemperatureUnits(_enum.Enum):
    CELSIUS = 0
    FAHRENHEIT = 1

    @classmethod
    def default(cls) -> Self:
        return cls.CELSIUS # type: ignore


# section 3.6.1
class EulerUnits(_enum.Enum):
    DEGREES = 0
    RADIANS = 1

    @classmethod
    def default(cls) -> Self:
        return cls.DEGREES # type: ignore


# section 3.6.1
class GyroUnits(_enum.Enum):
    # degrees per seconds
    DEG_PER_SEC = 0
    # radians
    RAD_PER_SEC = 1

    @classmethod
    def default(cls) -> Self:
        return cls.DEG_PER_SEC # type: ignore


# section 3.6.1
class AccUnits(_enum.Enum):
    # m/s^2
    METER_PER_S2 = 0
    MILLIGRAM = 1

    @classmethod
    def default(cls) -> Self:
        return cls.METER_PER_S2 # type: ignore


# section 3.6.1, 3.6.2, 4.3.60
class UnitSelection:
    """
    # Sample Code
    ```python
    unit_sel = UnitSelection()
        .set(UnitSelection.ORI_ANDROID)  # or .orientation_android()
        .set(UnitSelection.TEMP_CELSIUS) # or .temperature_celsius()
        .set(UnitSelection.EUL_RADIANS)  # or .euler_radians()
        .set(UnitSelection.GYR_RPS)      # or .gyroscope_rps()
        .set(UnitSelection.ACC_MPS2)     # or .acceleration_mps2

    assert unit_sel.orientation == UnitSelection.ORI_ANDROID
    assert unit_sel.value == 0b1000_0110
    ```
    """

    UnitsType = OrientationUnits | TemperatureUnits | EulerUnits | GyroUnits | AccUnits

    ORI_WINDOWS = OrientationUnits.WINDOWS
    ORI_ANDROID = OrientationUnits.ANDROID

    TEMP_CELSIUS = TemperatureUnits.CELSIUS
    TEMP_FAHRENHEIT = TemperatureUnits.FAHRENHEIT

    EUL_DEGREES = EulerUnits.DEGREES
    EUL_RADIANS = EulerUnits.RADIANS

    GYR_DPS = GyroUnits.DEG_PER_SEC
    GYR_RPS = GyroUnits.RAD_PER_SEC

    ACC_MPS2 = AccUnits.METER_PER_S2
    ACC_MILLIGRAM = AccUnits.MILLIGRAM

    def __init__(self) -> None:
        self._orientation: OrientationUnits = OrientationUnits.default()
        self._temperature: TemperatureUnits = TemperatureUnits.default()
        self._euler: EulerUnits = EulerUnits.default()
        self._gyroscope: GyroUnits = GyroUnits.default()
        self._acceleration: AccUnits = AccUnits.default()

    @property
    def value(self) -> int:
        ori: int = self._orientation.value << 7
        temp: int = self._temperature.value << 4
        eul: int = self._euler.value << 2
        gyr: int = self._gyroscope.value << 1
        acc: int = self._acceleration.value << 0
        return ori | temp | eul | gyr | acc

    def set(self, v: UnitsType) -> Self:
        match v:
            case UnitSelection.ORI_WINDOWS | UnitSelection.ORI_ANDROID:
                self._orientation = v
            case UnitSelection.TEMP_CELSIUS | UnitSelection.TEMP_FAHRENHEIT:
                self._temperature = v
            case UnitSelection.EUL_DEGREES | UnitSelection.EUL_RADIANS:
                self._euler = v
            case UnitSelection.GYR_DPS | UnitSelection.GYR_RPS:
                self._gyroscope = v
            case UnitSelection.ACC_MPS2 | UnitSelection.ACC_MILLIGRAM:
                self._acceleration = v
        return self

    @property
    def orientation(self) -> OrientationUnits:
        return self._orientation

    @property
    def temperature(self) -> TemperatureUnits:
        return self._temperature

    @property
    def euler(self) -> EulerUnits:
        return self._euler

    @property
    def gyroscope(self) -> GyroUnits:
        return self._gyroscope

    @property
    def acceleration(self) -> AccUnits:
        return self._acceleration

    def orientation_windows(self) -> Self:
        return self.set(UnitSelection.ORI_WINDOWS)

    def orientation_android(self) -> Self:
        return self.set(UnitSelection.ORI_ANDROID)

    def temperature_celsius(self) -> Self:
        return self.set(UnitSelection.TEMP_CELSIUS)

    def temperature_fahrenheit(self) -> Self:
        return self.set(UnitSelection.TEMP_FAHRENHEIT)

    def euler_degrees(self) -> Self:
        return self.set(UnitSelection.EUL_DEGREES)

    def euler_radians(self) -> Self:
        return self.set(UnitSelection.EUL_RADIANS)

    def gyroscope_dps(self) -> Self:
        return self.set(UnitSelection.GYR_DPS)

    def gyroscope_rps(self) -> Self:
        return self.set(UnitSelection.GYR_RPS)

    def acceleration_mps2(self) -> Self:
        return self.set(UnitSelection.ACC_MPS2)

    def acceleration_milligram(self) -> Self:
        return self.set(UnitSelection.ACC_MILLIGRAM)

    @classmethod
    def from_value(cls, value: int) -> Self:
        ori = OrientationUnits((value >> 7) & 1)
        temp = TemperatureUnits((value >> 4) & 1)
        eul = EulerUnits((value >> 2) & 1)
        gyr = GyroUnits((value >> 1) & 1)
        acc = AccUnits((value >> 0) & 1)
        return UnitSelection().set(ori).set(temp).set(eul).set(gyr).set(acc) # type: ignore
