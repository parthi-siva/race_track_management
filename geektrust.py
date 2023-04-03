from sys import argv
from src.racetrack import parse_command

def main():
    if len(argv) != 2:
        raise Exception("File path not entered")
    file_path = argv[1]
    f = open(file_path, 'r')
    Lines = f.readlines()
    result, total_bookings = parse_command(Lines)
    print("\n".join(result))
    print(f"{total_bookings.revenue_from_regular_track()} {total_bookings.revenue_from_vip_track()}")

if __name__ == "__main__":
    main()