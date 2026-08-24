from enum import Enum
from typing import NamedTuple, Optional

from PIL.Image import Image


class ValueRange(NamedTuple):
    min: float
    max: float


class Offset(NamedTuple):
    x: int  # from the left
    y: int  # from the top


class VisualElement(NamedTuple):
    image: Image
    relative_offset: Optional[Offset] = Offset(x=0, y=0)


class Color(NamedTuple):
    red: int
    green: int
    blue: int


class Category(Enum):
    ATP = "ATP"
    WTA = "WTA"
    ITF = "ITF"


class Surface(Enum):
    HARD = "Hard"
    GRASS = "Grass"
    CLAY = "Clay"
    CARPET = "Carpet"
    ALL = "All"
    ACRYLIC = "Acrylic"


class SurfaceCode(Enum):
    ALL = 0
    HARD = 2
    GRASS = 4
    CLAY = 8


class ShotType(Enum):
    FH = "FH"
    BH = "BH"


class MovementType(Enum):
    STATIONARY = "Stationary"
    RUNNING = "Running"


class Fonts(Enum):
    SEGO_UI = "SEGOEUI"
    SEGO_UI_BOLD = "SEGOEUIB"
    DIN = "DIN"


class CourtSide(Enum):
    DEUCE = "Deuce"
    AD = "Ad"


class ServeDirection(Enum):
    WIDE = "Wide"
    BODY = "Body"
    T = "T"


class ReturnDirection(Enum):
    CROSS = "Cross"
    MIDDLE = "Middle"
    LINE = "Line"


class Serve(Enum):
    FIRST = "First"
    SECOND = "Second"


class ServeStat(Enum):
    IN = "InAll"
    MISS = "Missed"
    WON = "WonServe"
    TOTAL_CROSS = "TotalCrossOpponentReturns"
    WON_CROSS = "WonCrossOpponentReturns"
    TOTAL_MIDDLE = "TotalMiddleOpponentReturns"
    WON_MIDDLE = "WonMiddleOpponentReturns"
    TOTAL_LINE = "TotalLineOpponentReturns"
    WON_LINE = "WonLineOpponentReturns"
    RETURN = "Return"
    IN_RETURN = "InReturn"
    WON_RETURN = "WonReturn"
    ACES = "Aces"


class StatType(Enum):
    BASIC = "Basic"
    SMHC = "SMHC"
    SPEED = "Speed"


class PointType(Enum):
    NORMAL = "ServeBasicStats"
    BREAK = "BreakServeBasicStats"
    PRESSURE = "PressureServeBasicStats"
    NON_PRESSURE = "NonPressureServeBasicStats"
    # Return Related
    RETURN_NORMAL = "ReturnBasicStats"
    RETURN_BREAK = "BreakReturnBasicStats"
    RETURN_PRESSURE = "PressureReturnBasicStats"
    RETURN_NON_PRESSURE = "NonPressureReturnBasicStats"
    # Speed related
    SPEED_ALL = "AllServeSpeedStats"


class Distribution(Enum):
    AVG = "Average"
    MED = "Median"
    HI = "High"
    LO = "Low"


class GameSelection(Enum):
    WON = "Won"
    LOST = "Lost"
    ALL = "All"

class SetSelection(Enum):
    WON = "Won"
    LOST = "Lost"
    ALL = "All"

class ServeSelection(Enum):
    SERVER = "Server"
    RETURNER = "Returner"
    ALL = "All"
