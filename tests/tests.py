import os
import unittest
from src.racetrack import parse_command


class TestGeekTrust(unittest.TestCase):
    def test_race_track_management_book_for_invalid_time(self):
        """For times befor 1.00pm and after 8.00pm it should
        return INVALID_ENTRY_TIME"""
        command = ["BOOKSUV A66 11:00"]
        result, _ = parse_command(command)
        self.assertEquals(result[0], "INVALID_ENTRY_TIME")

    def test_race_track_management_addtional_time_for_invalid_time(self):
        command = ["BOOK BIKE M40 14:00", "ADDITIONAL M40 17:40"]
        result, _ = parse_command(command)
        self.assertEquals(result[1], "INVALID_ENTRY_TIME")

    def test_race_track_management_for_race_track_full_for_bike(self):
        """For bike max no is 4. This test ensure that"""
        command = [
            "BOOK BIKE M40 14:00",
            "BOOK BIKE M40 13:00",
            "BOOK BIKE M40 15:00",
            "BOOK BIKE M40 16:00",
            "BOOK BIKE M40 16:15",
        ]
        result, _ = parse_command(command)
        self.assertEquals(result[4], "RACETRACK_FULL")

    def test_race_track_management_for_race_track_full_for_car(self):
        """"""
        command = [
            "BOOK CAR AB1 14:20",
            "BOOK CAR AB2 14:30",
            "BOOK CAR AB3 14:40",
            "BOOK CAR AB4 14:50",
        ]
        result, _ = parse_command(command)
        self.assertEquals(result[3], "RACETRACK_FULL")

    def test_race_track_management_for_race_track_full_for_suv(self):
        command = [
            "BOOK SUV AB1 14:20",
            "BOOK SUV AB2 14:30",
            "BOOK SUV AB3 14:40",
            "BOOK SUV AB4 14:50",
        ]
        result, _ = parse_command(command)
        self.assertEquals(result[3], "RACETRACK_FULL")


if __name__ == "__main__":
    unittest.main()
