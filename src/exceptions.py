class BookingFullException(Exception):
    """Exception raised when race track for car is Full"""

class InvalidEntryTimeException(Exception):
    """Exception raised when booking time is beyond allowable range"""

class InvalidExitTimeException(Exception):
    """Exception raised when booking time is beyond allowable range"""
