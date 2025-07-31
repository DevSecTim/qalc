import re
from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar


@dataclass(frozen=True, eq=True)
class TimeFrame:
    """
    Immutable class representing a timeframe for market data.
    """

    amount: int
    unit: str

    def __post_init__(self):
        object.__setattr__(self, "unit", self.unit.lower())

    def __hash__(self):
        return hash((self.amount, self.unit))

    def __repr__(self):
        return f"{self.amount}_{self.unit}"

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.to_timedelta() - other
        elif isinstance(other, TimeFrame):
            return self.to_timedelta() - other.to_timedelta()
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, timedelta):
            return self.to_timedelta() + other
        elif isinstance(other, TimeFrame):
            return self.to_timedelta() + other.to_timedelta()
        else:
            return NotImplemented

    def to_alpaca(self):
        try:
            from alpaca.data.timeframe import TimeFrame as AlpacaTimeFrame
            from alpaca.data.timeframe import TimeFrameUnit as AlpacaTimeFrameUnit
        except ImportError:
            raise ImportError(
                "alpaca-py is not installed: Cannot convert to "
                "Alpaca-native TimeFrame."
            )

        unit_map = {
            "minute": AlpacaTimeFrameUnit.Minute,
            "hour": AlpacaTimeFrameUnit.Hour,
            "day": AlpacaTimeFrameUnit.Day,
            "week": AlpacaTimeFrameUnit.Week,
            "month": AlpacaTimeFrameUnit.Month,
        }
        return AlpacaTimeFrame(self.amount, unit_map[self.unit])

    def to_timedelta(self):
        if self.unit == "minute":
            return timedelta(minutes=self.amount)
        elif self.unit == "hour":
            return timedelta(hours=self.amount)
        elif self.unit == "day":
            return timedelta(days=self.amount)
        elif self.unit == "week":
            return timedelta(weeks=self.amount)
        else:
            raise ValueError(f"Cannot convert {self} to timedelta")

    @classmethod
    def from_string(cls, s: str) -> "TimeFrame":
        """
        Factory method to create a TimeFrame from a string like '1Min', '5Min',
        '1Hour', '1Day', etc.
        """
        s = s.strip().lower()

        match = re.match(r"(\d+)(min|minute|hour|day|week|month)s?", s)
        if not match:
            raise ValueError(f"Invalid timeframe string: {s}")
        amount = int(match.group(1))
        unit = match.group(2)
        if unit == "min":
            unit = "minute"
        return cls(amount, unit)

    # Predefined constants (enum-like)
    MINUTE: ClassVar["TimeFrame"]
    FIVE_MINUTES: ClassVar["TimeFrame"]
    FIFTEEN_MINUTES: ClassVar["TimeFrame"]
    HOUR: ClassVar["TimeFrame"]
    DAY: ClassVar["TimeFrame"]
    WEEK: ClassVar["TimeFrame"]
    MONTH: ClassVar["TimeFrame"]


TimeFrame.MINUTE = TimeFrame(1, "minute")
TimeFrame.FIVE_MINUTES = TimeFrame(5, "minute")
TimeFrame.FIFTEEN_MINUTES = TimeFrame(15, "minute")
TimeFrame.HOUR = TimeFrame(1, "hour")
TimeFrame.DAY = TimeFrame(1, "day")
TimeFrame.WEEK = TimeFrame(1, "week")
TimeFrame.MONTH = TimeFrame(1, "month")
