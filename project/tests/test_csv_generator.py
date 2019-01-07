import collections
import csv
import os

import nose
import sys
import unittest
from StringIO import StringIO
from contextlib import contextmanager

from project.lib.csv_generator import CsvGenerator


class TestCsvGenerator(unittest.TestCase):

    def setUp(self):
        self.csv_generator = CsvGenerator()

    def test_project_should_generate_leads(self):
        res = self.csv_generator.generate_leads_file(2, None)
        print(res)
        assert len(res) == 3
        header = res[0]
        assert header[0] == 'Email'
        assert header[1] == 'First Name'
        assert header[2] == 'Last Name'

    def test_project_should_generate_leads_file(self):
        lines = 12
        outfile = open(str(lines) + '.csv', 'w+')
        self.csv_generator.generate_leads_file(lines, outfile, 10)
        outfile.close()

        with open(os.path.abspath(outfile.name)) as res:
            reader = csv.DictReader(res, delimiter=',')
            header = reader.fieldnames
            assert header[0] == 'Email'
            assert header[1] == 'First Name'
            assert header[2] == 'Last Name'
            counter = 0
            for row in reader:
                print(row)
                counter += 1
            assert counter == lines

        try:
            os.remove(os.path.abspath(outfile.name))
        except OSError:
            pass

    def test_project_should_generate_leads_file_main_method(self):

        file_name = "2.csv"
        sys.argv = ["generate", "generate", "-r", "2", "-o", file_name, "-b", "1000", "--verbose"]
        with open(os.path.abspath("2.csv"), "w+") as out_file:
            res = self.csv_generator.generate_leads_file(2, out_file, 1000)
            assert res is None
            os.path.isfile(file_name)
            try:
                os.remove(os.path.abspath(file_name))
            except OSError:
                pass

    def test_project_should_generate_leads_filename(self):
        lines = 12
        filename = str(lines) + '.csv'

        # Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        # opts = Options(filename, str(lines), True, '100')
        with open(os.path.abspath(filename), "w+") as res:
            self.csv_generator.generate_leads_file(12, res, 100)

        with open(os.path.abspath(filename)) as res:

            reader = csv.DictReader(res, delimiter=',')
            header = reader.fieldnames
            assert header[0] == 'Email'
            assert header[1] == 'First Name'
            assert header[2] == 'Last Name'
            counter = 0
            for row in reader:
                print(row)
                counter += 1
            assert counter == lines

        try:
            os.remove(os.path.abspath(filename))
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
