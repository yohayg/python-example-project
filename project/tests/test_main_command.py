import csv
import os
import sys
import time
import unittest
from StringIO import StringIO
from contextlib import contextmanager

import nose
from progress.bar import Bar

from project.lib.csv_rx_generator import generate_data
from project.lib.csv_rx_generator import print_thread
from project.lib.csv_rx_generator import print_thread_close_file
from project.lib.main_command import MainCommand


def check_file_content(lines, file_name):
    print("checking file content at: " + file_name)
    with open(os.path.abspath(file_name)) as res:
        reader = csv.DictReader(res, delimiter=',')
        header = reader.fieldnames
        assert header[0] == 'Email'
        assert header[1] == 'First Name'
        assert header[2] == 'Last Name'
        counter = 0
        for row in reader:
            print(row)
            counter += 1
        print("%s %s" % (counter, lines))
        assert counter == lines


class TestMainCommand(unittest.TestCase):

    def setUp(self):
        self.main_command = MainCommand()

    def test_main_csv_se(self):

        lines = 20
        file_name = str(lines) + '.csv'
        sys.argv = ["csv-gen", "se", "--rows", "20", "-o", file_name, "-b", "1000", "--verbose"]

        self.main_command.main()

        time.sleep(5)
        os.path.isfile(os.path.abspath(file_name))

        check_file_content(lines, os.path.abspath(file_name))

        try:
            os.remove(os.path.abspath(file_name))
        except OSError:
            pass

    def test_main_csv_rx(self):
        # Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])

        lines = 20
        file_name = str(lines) + '.csv'
        sys.argv = ["csv-gen", "rx", "--rows", "20", "-o", file_name, "-b", "1000", "--verbose"]
        self.main_command.main()

        time.sleep(5)
        os.path.isfile(os.path.abspath(file_name))

        check_file_content(lines, os.path.abspath(file_name))

        try:
            os.remove(os.path.abspath(file_name))
        except OSError:
            pass

    def test_main_csv_mp(self):
        self.run_command_options("se", 20)

    def run_command_options(self, command, lines):
        # Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        file_name = command + str(lines) + '.csv'
        sys.argv = ["csv-gen", "mp", "--rows", "20", "-o", file_name, "-b", "1000", "--verbose"]
        self.main_command.main()
        time.sleep(5)
        os.path.isfile(os.path.abspath(file_name))
        check_file_content(lines, os.path.abspath(file_name))
        try:
            os.remove(os.path.abspath(file_name))
        except OSError:
            pass

    def test_project_should_generate_leads_file_total_greater_then_bulk(self):
        # Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])

        lines = 20
        file_name = str(lines) + '.csv'
        sys.argv = ["csv-gen", "se", "-r", "20", "-o", file_name, "-b", "9", "--verbose"]
        self.main_command.main()

        time.sleep(5)
        os.path.isfile(os.path.abspath(file_name))

        check_file_content(lines, os.path.abspath(file_name))

        try:
            os.remove(os.path.abspath(file_name))
        except OSError:
            pass

    def test_generate_data(self):
        res = generate_data(5, 1)
        assert len(res) == 5

    def test_print_thread(self):
        print_thread('hello')
        assert True

    def test_print_thread_close_file(self):
        progress_bar = Bar('Generating', fill='#', suffix='%(percent)d%% - %(elapsed_td)s', max=5)
        outfile = open("temp.txt", 'w+')
        print_thread_close_file("error msg", outfile, progress_bar)

        assert outfile.closed
        try:
            os.remove(os.path.abspath(outfile.name))
        except OSError:
            pass


@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


if __name__ == '__main__':
    nose.run()
