from enum import Enum


class FuelType(str, Enum):
    FLEX = "flex"
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ETHANOL = "ethanol"
    ELECTRIC = "electric"
    HYBRID = "hybrid"


class TransmissionType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    CVT = "cvt"
    AUTOMATED_MANUAL = "automated_manual"


class SortField(str, Enum):
    ID = "id"
    PRICE = "price"
    YEAR = "year"
    MILEAGE = "mileage"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"