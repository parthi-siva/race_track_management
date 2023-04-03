from src.exceptions import (BookingFullException, InvalidEntryTimeException,
                         InvalidExitTimeException)
from src.models import TotalBookings, Status
from src.utils import (create_booking, update_booking, validate_additional_time,
                    validate_booking_timing)

BOOK_COMMAND_LEN = 4
UPDATE_BOOK_COMMAND_LEN = 3

class CommandParseFactory:
    def build_booking(self, vehicle_number, booking_time, vehicle_type):
        return BookTrack(
            vehicle_number=vehicle_number,
            booking_time=booking_time,
            vehicle_type=vehicle_type,
        )

    def build_update_booking(self, vehicle_number, booking_time):
        return UpdateBooking(vehicle_number=vehicle_number, booking_time=booking_time)


command_factory_obj = CommandParseFactory()


def load(commands, factory):
    command_obj = []
    for command in commands:
        command_list = command.strip().split(" ")
        if len(command_list) == BOOK_COMMAND_LEN:
            _, vehicle_type, vehicle_number, booking_time = command_list
            command_obj.append(
                factory.build_booking(vehicle_number, booking_time, vehicle_type)
            )
        elif len(command_list) == UPDATE_BOOK_COMMAND_LEN:
            _, vehicle_number, booking_time = command_list
            command_obj.append(
                factory.build_update_booking(vehicle_number, booking_time)
            )
    return command_obj


def apply_command(command_objs):
    total_bookings = TotalBookings()
    result = []
    for command in command_objs:
        if isinstance(command, BookTrack):
            try:
                command.book(total_bookings)
                result.append(Status.SUCCESS.value)
            except InvalidEntryTimeException:
                result.append(Status.INVALID_ENTRY_TIME.value)
            except BookingFullException:
                result.append(Status.RACETRACK_FULL.value)
        elif isinstance(command, UpdateBooking):
            try:
                command.update(total_bookings)
                result.append(Status.SUCCESS.value)
            except InvalidExitTimeException:
                result.append(Status.INVALID_EXIT_TIME.value)
            except BookingFullException:
                result.append(Status.RACETRACK_FULL.value)
    return result, total_bookings


def parse_command(commands):
    c = load(commands, command_factory_obj)
    result, total_bookings = apply_command(c)
    return result, total_bookings


class BookTrack:
    def __init__(self, vehicle_number, vehicle_type, booking_time):
        self.vehicle_number = vehicle_number
        self.vehicle_type = vehicle_type
        self.booking_time = booking_time

    def book(self, total_bookings):
        validate_booking_timing(self.booking_time)
        create_booking(
            vehicle_number=self.vehicle_number,
            vehicle_type=self.vehicle_type,
            booking_time=self.booking_time,
            total_bookings=total_bookings,
        )


class UpdateBooking:
    def __init__(self, vehicle_number, booking_time):
        self.vehicle_number = vehicle_number
        self.booking_time = booking_time

    def update(self, total_bookings):
        validate_additional_time(self.booking_time)
        update_booking(
            vehicle_number=self.vehicle_number,
            booking_time=self.booking_time,
            total_bookings=total_bookings,
        )
