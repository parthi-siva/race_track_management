import unittest
from .context import racetrack, models


class TestRaceTrackManagement(unittest.TestCase):
    def test_race_track_management_book_for_less_than_13_00_pm(self):
        """
            For times befor 1.00pm and after 8.00pm it should
            return INVALID_ENTRY_TIME
        """
        command = ["BOOK SUV A66 11:00"]
        result, _ = racetrack.parse_command(command)
        self.assertEqual(result[0], models.Status.INVALID_ENTRY_TIME.value)

    def test_race_track_management_book_for_greater_than_20_00_pm(self):
        command = ["BOOK SUV A66 21:00"]
        result, _ = racetrack.parse_command(command)
        self.assertEqual(result[0], models.Status.INVALID_ENTRY_TIME.value)

    def test_race_track_management_for_race_track_full_for_bike(self):
        """For bike max no is 4. This test ensure that"""
        command = [
            "BOOK BIKE M40 14:00",
            "BOOK BIKE M40 13:00",
            "BOOK BIKE M40 15:00",
            "BOOK BIKE M40 16:00",
            "BOOK BIKE M40 16:15",
        ]
        result, _ = racetrack.parse_command(command)
        self.assertEqual(result[4], models.Status.RACETRACK_FULL.value)

    def test_race_track_management_for_race_track_full_for_car(self):
        command = [
            "BOOK CAR AB1 14:20",
            "BOOK CAR AB2 14:30",
            "BOOK CAR AB3 14:40",
            "BOOK CAR AB4 14:50",
        ]
        result, _ = racetrack.parse_command(command)
        self.assertEqual(result[3], models.Status.RACETRACK_FULL.value)

    def test_race_track_management_for_race_track_full_for_suv(self):
        command = [
            "BOOK SUV AB1 14:20",
            "BOOK SUV AB2 14:30",
            "BOOK SUV AB3 14:40",
            "BOOK SUV AB4 14:50",
        ]
        result, _ = racetrack.parse_command(command)
        self.assertEqual(result[3], models.Status.RACETRACK_FULL.value)

    def test_race_track_management_for_booking_time_close_to_end_time(self):
        """
            Since end time is 8.00 PM and minimum bookings time is 3 hours
            So if someone tries to book after 6.00 PM we should return invalid time.
            This test ensures that
        """
        command = ["BOOK SUV A66 18:00"]
        result, _ = racetrack.parse_command(command)
        self.assertEqual(result[0], models.Status.INVALID_ENTRY_TIME.value)

    def test_race_track_management_for_additional_booking_time(self):
        command = ["BOOK BIKE BIK2 14:00","ADDITIONAL BIK2 17:50"]
        result, tot = racetrack.parse_command(command)
        self.assertEqual(tot.revenue_from_regular_track(), 230)
        self.assertEqual(result[1], models.Status.SUCCESS.value)

    def test_race_track_management_for_additional_booking_time_less_than_15_mins(self):
        command = ["BOOK BIKE BIK2 14:00","ADDITIONAL BIK2 17:10"]
        result, tot = racetrack.parse_command(command)
        self.assertEqual(tot.revenue_from_regular_track(), 180)
        self.assertEqual(result[1], models.Status.SUCCESS.value)

    def test_race_track_management_allocates_vip_track(self):
        """If Regular track is full for cars/suv then we should
        allocate VIP track if available"""
        command = [
            "BOOK CAR AB1 14:20",
            "BOOK CAR AB2 14:30",
            "BOOK CAR AB3 14:40",
        ]
        result, tot = racetrack.parse_command(command)
        self.assertEqual(tot.revenue_from_vip_track(), 750)
        self.assertEqual(result[2], models.Status.SUCCESS.value)

if __name__ == "__main__":
    unittest.main()
