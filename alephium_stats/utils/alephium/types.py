from enum import Enum


class TimeInterval(Enum):
    DAILY = "daily"
    HOURLY = "hourly"
    WEEKLY = "weekly"


class SupplyType(Enum):
    TOTAL = "total"
    CIRCULATING = "circulating"
    RESERVED = "reserved"
    LOCKED = "locked"
