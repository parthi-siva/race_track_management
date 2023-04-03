import operator
from datetime import datetime, timedelta

from src.exceptions import (BookingFullException, InvalidEntryTimeException,
                         InvalidExitTimeException)
from src.models import (Booking, RaceTrackType, RegularTrackCapacity, VehicleType,
                     VIPTrackCapacity)

TRACK_OPENING_TIME = "13:00"
TRACK_CLOSING_TIME = "20:00"


def _create_booking_object(
    vehicle_number, vehicle_type, booking_time, track_type, total_bookings
):
    booking_time = parse_time(booking_time)
    vehicle_type = operator.attrgetter(vehicle_type)(VehicleType)
    booking = Booking(
        vehicle_number=vehicle_number,
        vehicle_type=vehicle_type,
        booking_time=booking_time,
        track_type=track_type,
    )
    total_bookings.add_bookings(booking)
    total_bookings.update_active_bookings(booking_time)
    return booking


def validate_booking_timing(booking_time):
    booking_time = parse_time(booking_time)
    opening_hour, opening_mins = map(int, TRACK_OPENING_TIME.split(":"))
    track_opentime = create_datetime(opening_hour, opening_mins)
    closing_hour, closing_mins = map(int, TRACK_CLOSING_TIME.split(":"))
    track_closing_time = create_datetime(closing_hour, closing_mins)
    if booking_time < track_opentime:
        raise InvalidEntryTimeException("Booking time should be after 1.00 PM")
    elif booking_time + timedelta(hours=3) > track_closing_time:
        raise InvalidEntryTimeException("Booking time should be before 6.00 PM")
    elif booking_time > track_closing_time:
        raise InvalidExitTimeException("Booking time should be less than 8.00 PM")


def validate_additional_time(booking_time):
    booking_time = parse_time(booking_time)
    closing_hour, closing_mins = map(int, TRACK_CLOSING_TIME.split(":"))
    track_closing_time = create_datetime(closing_hour, closing_mins)
    if booking_time > track_closing_time:
        raise InvalidExitTimeException("Booking time should be less than 8.00 PM")


def create_booking(vehicle_number, vehicle_type, booking_time, total_bookings):
    if total_bookings is None:
        return _create_booking_object(
            vehicle_number,
            vehicle_type,
            booking_time,
            RaceTrackType.REGULAR,
            total_bookings,
        )
    elif vehicle_type == VehicleType.BIKE.value:
        return create_bike_booking(
            vehicle_number, vehicle_type, booking_time, total_bookings
        )
    else:
        return create_regular_car_booking(
            vehicle_number, vehicle_type, booking_time, total_bookings
        )


def create_regular_car_booking(
    vehicle_number, vehicle_type, booking_time, total_bookings
):
    regular_booking_count = get_booked_vehicle_count(
        total_bookings, vehicle_type, "REGULAR", booking_time
    )
    if (
        regular_booking_count
        < operator.attrgetter(vehicle_type)(RegularTrackCapacity).value
    ):
        return _create_booking_object(
            vehicle_number,
            vehicle_type,
            booking_time,
            RaceTrackType.REGULAR,
            total_bookings,
        )
    else:
        return create_vip_car_booking(
            vehicle_number, vehicle_type, booking_time, total_bookings
        )


def create_vip_car_booking(vehicle_number, vehicle_type, booking_time, total_bookings):
    regular_booking_count = get_booked_vehicle_count(
        total_bookings, vehicle_type, "VIP", booking_time
    )
    if (
        regular_booking_count
        < operator.attrgetter(vehicle_type)(VIPTrackCapacity).value
    ):
        return _create_booking_object(
            vehicle_number,
            vehicle_type,
            booking_time,
            RaceTrackType.VIP,
            total_bookings,
        )
    else:
        raise BookingFullException


def create_bike_booking(vehicle_number, vehicle_type, booking_time, total_bookings):
    bike_booking_count = get_booked_vehicle_count(
        total_bookings, vehicle_type, "REGULAR", booking_time
    )
    if (
        bike_booking_count
        < operator.attrgetter(vehicle_type)(RegularTrackCapacity).value
    ):
        return _create_booking_object(
            vehicle_number,
            vehicle_type,
            booking_time,
            RaceTrackType.REGULAR,
            total_bookings,
        )
    else:
        raise BookingFullException


def is_booking_expired(active_bookings, vehicle_type, booking_time, track_type):
    vehicle_list = filter_vehicle_list(active_bookings, vehicle_type, track_type)
    hour, mins = map(int, booking_time.split(":"))
    return list(
        filter(
            lambda x: x.booking_time + timedelta(hours=x.hours)
            <= create_datetime(hour, mins),
            vehicle_list,
        )
    )


def get_booked_vehicle_count(booking_list, vehicle_type, track_type, booking_time):
    return len(
        filter_vehicle_list(booking_list.gross_bookings, vehicle_type, track_type)
    ) - len(
        is_booking_expired(
            booking_list.current_active_bookings, vehicle_type, booking_time, track_type
        )
    )


def filter_vehicle_list(booking_list, vehicle_type, track_type):
    return list(
        filter(
            lambda b: b.vehicle_type.value == vehicle_type
            and b.track_type.value == track_type,
            booking_list,
        )
    )


def create_datetime(hour, minute):
    today = datetime.today()
    return datetime(
        year=today.year, month=today.month, day=today.day, hour=hour, minute=minute
    )


def find_previous_booking(vehicle_number, bookings_list):
    previous_booking = next(
        filter(
            lambda b: b.vehicle_number == vehicle_number, bookings_list.gross_bookings
        )
    )
    return previous_booking


def _update_booking(booking_obj, booking_time, extra_hours):
    booking_obj.booking_time = parse_time(booking_time)
    previous_cost = booking_obj.cost()
    booking_obj.cost = lambda *args, **kwargs: previous_cost + extra_hours * 50
    booking_obj.hours += extra_hours


def update_booking(vehicle_number, total_bookings, booking_time):
    booking = find_previous_booking(vehicle_number, total_bookings)
    if booking:
        extra_hours = compute_extra_hours(booking, booking_time)
        _update_booking(booking, booking_time, extra_hours)


def parse_time(booking_time):
    hour, mins = map(int, booking_time.split(":"))
    return create_datetime(hour, mins)


def compute_booking_time_diff(booking, booking_time):
    booking_time = parse_time(booking_time)
    return booking_time - booking.booking_time


def compute_extra_hours(booking, booking_time):
    additional_time = compute_booking_time_diff(booking, booking_time)
    extra_hour = 0
    if parse_time(booking_time) > booking.booking_time + timedelta(hours=3, minutes=15):
        hour2, _, _ = map(int, str(additional_time).split(":"))
        extra_hour = (hour2 - booking.hours) + 1
    return extra_hour
