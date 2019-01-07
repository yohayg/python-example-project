import sys

from lib.main_command import MainCommand


def main():
    csv_generator = MainCommand()
    sys.exit(csv_generator.main())


if __name__ == "__main__":
    main()
