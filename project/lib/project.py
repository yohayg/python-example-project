import csv
import os
import sys
import time

from faker import Faker

from process import Process


class Project:

    def __init__(self, options):
        self.options = options
        self.process = Process()

    def date(self):
        return self._get_date()

    def _get_date(self):
        # prints stdout of subprocess with command "date"
        # strips tailing end of lines because print adds one
        return self.process.execute("date").rstrip('\n')

    def print_example_arg(self):
        return self.options.known.example

    @staticmethod
    def progress(count, total_number, status=''):

        bar_len = 60
        filled_len = int(round(bar_len * count / float(total_number)))

        percents = round(100.0 * count / float(total_number), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush()
        if count == total_number:
            print ''

    def generate_leads(self, total, output_file):

        if output_file is None:
            return None
        else:
            outfile = open(output_file, 'w+')
            res = self.generate_leads_file(total, outfile)
            outfile.close()
            return res

    def generate_leads_file(self, total, outfile):

        fake = Faker()
        start_time = time.time()

        result = None
        outfile_writer = None
        if outfile is None:
            print 'Generating ', total, ' leads.'
            result = []
        else:
            print 'Generating ', total, ' leads. Output file:', os.path.abspath(outfile.name)
            outfile_writer = csv.writer(outfile, delimiter=',')

        print ''

        header = ['Email', 'First Name', 'Last Name']

        if outfile is None:
            result.append(header)
        else:
            outfile_writer.writerow(header)

        bulk_lines = []
        bulk_size = 1000
        for i in range(total):

            first = str(fake.first_name())
            last = str(fake.last_name())
            email = str(fake.email())

            line = [email, first, last]
            # id = str(uuid.uuid4())
            # line.append(id)
            elapsed_time = time.time() - start_time
            elapsed_time_str = str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
            self.progress(i, total, status=elapsed_time_str)
            bulk_lines.append(line)
            if outfile is None:
                result.append(line)

            if len(bulk_lines) == bulk_size:
                outfile_writer.writerows(bulk_lines)
                bulk_lines = []

        # write the rest
        if len(bulk_lines) > 0:
            if outfile is not None:
                outfile_writer.writerows(bulk_lines)
        self.progress(total, total, status='done')

        return result
