import csv
import os
import unittest

from mockito import mock, when, verify

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
        mocked_process = mock()
        when(mocked_process).execute('date').thenReturn("The date might be: "
                                                        + self.project.process.execute("date").strip('\n')
                                                        + "\nbut we could also overwrite it to be the"
                                                        + " 1st of April instead.")
        # overwriting project's process.execute('date') with the mock function above
        # just an example of overwriting a dependency when testing
        self.project.process = mocked_process

    def test_project_should_get_date(self):
        self.assertTrue('1st of April' in self.project.process.execute('date'))
        verify(self.project.process).execute('date')

    def test_project_should_generate_leads(self):
        self.project = Project(self._default_options())
        res = self.project.generate_leads_file(2, None)
        print res
        assert len(res) == 3
        header = res[0]
        assert header[0] == 'Email'
        assert header[1] == 'First Name'
        assert header[2] == 'Last Name'

    def test_project_should_generate_leads_file(self):
        self.project = Project(self._default_options())

        outfile = open('2.csv', 'w+')
        self.project.generate_leads_file(2, outfile)
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
            assert counter == 2

        try:
            os.remove(os.path.abspath(outfile.name))
        except OSError:
            pass

    def test_project_should_generate_leads_null_file(self):
        self.project = Project(self._default_options())
        res = self.project.generate_leads(2, None)
        print res
        assert res is None


if __name__ == '__main__':
    unittest.main()
