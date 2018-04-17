import csv
import os
import unittest

from project.lib import Options
from project.lib import Project


class TestProject(unittest.TestCase):

    @staticmethod
    def _default_options():
        options = Options()
        options.parse()
        return options

    def setUp(self):
        self.project = Project(self._default_options())

    def test_project_should_generate_leads(self):
        res = self.project.generate_leads_file(2, None)
        print res
        assert len(res) == 3
        header = res[0]
        assert header[0] == 'Email'
        assert header[1] == 'First Name'
        assert header[2] == 'Last Name'

    def test_project_should_generate_leads_file(self):
        lines = 12
        outfile = open(str(lines)+'.csv', 'w+')
        self.project.generate_leads_file(lines, outfile, 10)
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

    def test_project_should_generate_leads_null_file(self):
        res = self.project.generate_leads(2, None)
        print res
        assert res is None

    def test_project_should_generate_leads_filename(self):
        lines = 12
        filename = str(lines) + '.csv'
        self.project.generate_leads(lines, filename)

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


if __name__ == '__main__':
    unittest.main()
