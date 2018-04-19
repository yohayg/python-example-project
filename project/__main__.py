import sys

from lib.csv_generator import CsvGenerator


def main():
    csv_generator = CsvGenerator()
    sys.exit(csv_generator.main())


if __name__ == "__main__":
    main()
