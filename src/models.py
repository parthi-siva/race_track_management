import operator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List

TRACK_OPENING_TIME = "13:00"
TRACK_CLOSING_TIME = "20:00"


class VehicleType(Enum):
    BIKE = "BIKE"
    CAR = "CAR"
    SUV = "SUV"


class RaceTrackType(Enum):
    REGULAR = "REGULAR"
    VIP = "VIP"


class RegularCost(Enum):
    BIKE = 60
    CAR = 120
    SUV = 200


class VIPCost(Enum):
    CAR = 250
    SUV = 300


class RegularTrackCapacity(Enum):
    BIKE = 4
    CAR = 2
    SUV = 2


class VIPTrackCapacity(Enum):
    CAR = 1
    SUV = 1


class Status(Enum):
    SUCCESS = "SUCCESS"
    RACETRACK_FULL = "RACETRACK_FULL"
    INVALID_ENTRY_TIME = "INVALID_ENTRY_TIME"
    INVALID_EXIT_TIME = "INVALID_EXIT_TIME"


@dataclass
class Booking:
    vehicle_number: str
    vehicle_type: VehicleType
    booking_time: datetime
    track_type: RaceTrackType
    hours: int = 3

    def cost(self):
        if self.track_type.value == "REGULAR":
            return (
                operator.attrgetter(self.vehicle_type.value)(RegularCost).value
                * self.hours
            )
        elif self.track_type.value == "VIP":
            return (
                operator.attrgetter(self.vehicle_type.value)(VIPCost).value * self.hours
            )


def create_datetime(hour, minute):
    today = datetime.today()
    return datetime(
        year=today.year, month=today.month, day=today.day, hour=hour, minute=minute
    )


@dataclass
class TotalBookings:
    gross_bookings: List[Booking] = field(default_factory=list)
    current_active_bookings: List[Booking] = field(default_factory=list)

    def add_bookings(self, booking):
        self.gross_bookings.append(booking)

    def update_active_bookings(self, booking_time):
        self.current_active_bookings = []
        for x in self.gross_bookings:
            if x.booking_time + timedelta(hours=x.hours) > booking_time:
                self.current_active_bookings.append(x)

    def revenue_from_regular_track(self):
        return sum(
            [
                booking.cost()
                for booking in filter(
                    lambda b: b.track_type == RaceTrackType.REGULAR, self.gross_bookings
                )
            ]
        )

    def revenue_from_vip_track(self):
        return sum(
            [
                booking.cost()
                for booking in filter(
                    lambda b: b.track_type == RaceTrackType.VIP, self.gross_bookings
                )
            ]
        )
