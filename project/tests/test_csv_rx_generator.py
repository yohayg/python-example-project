import collections
import csv
import os
import sys
import time
import unittest
import nose
from StringIO import StringIO
from contextlib import contextmanager

from project.lib.csv_rx_generator import CsvRxGenerator


class TestCsvRxGenerator(unittest.TestCase):

    def setUp(self):
        self.csv_rx_generator = CsvRxGenerator()

    def test_project_should_generate_leads_file(self):
        lines = 12
        file_name = str(lines) + '.csv'
        outfile = open(file_name, 'w+')
        CsvRxGenerator.generate_leads_file(lines, outfile)
        # outfile.close()
        time.sleep(5)
        outfile.close()

        self.check_file_content(lines, os.path.abspath(file_name))

        try:
            os.remove(os.path.abspath(outfile.name))
        except OSError:
            pass

    def check_file_content(self, lines, file_name):
        print("checking file content at: "+file_name)
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

    def test_project_should_generate_leads_file_main_method(self):
        # Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])

        lines = 20
        file_name = str(lines) + '.csv'
        sys.argv = ["generate", "generate", "-r", "20", "-o", file_name, "-b", "1000", "--verbose"]
        self.csv_rx_generator.main()

        time.sleep(5)
        os.path.isfile(os.path.abspath(file_name))

        self.check_file_content(lines, os.path.abspath(file_name))

        try:
            os.remove(os.path.abspath(file_name))
        except OSError:
            pass

    def test_project_should_generate_leads_empty_path(self):

        Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        opts = Options('', '2', False, '100')

        with captured_output() as (out, err):
            self.csv_rx_generator.do_generate_leads(None, opts, [])
            output = err.getvalue().strip()
            assert output == 'Path is missing or invalid'

    def test_project_should_generate_leads_invalid_path(self):

        Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        opts = Options("/neverland/2.csv", '2', False, '100')

        with captured_output() as (out, err):
            res = self.csv_rx_generator.do_generate_leads(None, opts, [])
            assert res is None
            output = err.getvalue().strip()
            assert output.split('\n')[0] == 'Path is invalid: /neverland/2.csv'

    def test_project_should_generate_leads_invalid_rows(self):

        Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        opts = Options('2.csv', 'ss', False, '100')

        with captured_output() as (out, err):
            self.csv_rx_generator.do_generate_leads(None, opts, [])
            output = err.getvalue().strip()
            assert output == 'Number of rows is invalid'

    def test_project_should_generate_leads_invalid_bulk(self):

        Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        opts = Options('2.csv', '2', False, 'ss')

        with captured_output() as (out, err):
            res = self.csv_rx_generator.do_generate_leads(None, opts, [])
            assert res is None
            output = err.getvalue().strip()
            assert output == 'Number of bulk is invalid'

    def test_project_should_generate_leads_filename(self):
        lines = 12
        filename = str(lines) + '.csv'

        Options = collections.namedtuple('Options', ['output', 'rows', 'verbose', 'bulk'])
        opts = Options(filename, str(lines), True, '100')

        self.csv_rx_generator.do_generate_leads(None, opts, [])

        time.sleep(5)

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
