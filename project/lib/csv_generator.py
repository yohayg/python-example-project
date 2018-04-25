from __future__ import print_function

import csv
import logging
import os

from faker import Faker
from progress.bar import Bar

from project.lib.data_generator import DataGenerator

log = logging.getLogger("CsvGenerator")


class CsvGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_leads_file(total, outfile, bulk_size=1000):

        result = None
        outfile_writer = None
        if outfile is None:
            print('Generating %s leads.' % total)
            result = []
        else:
            print('Generating %s leads. Output file: %s' % (total, os.path.abspath(outfile.name)))
            outfile_writer = csv.writer(outfile, delimiter=',')

        print('')

        header = ['Email', 'First Name', 'Last Name']

        if outfile is None:
            result.append(header)
        else:
            outfile_writer.writerow(header)

        bulk_lines = []

        progress_bar = Bar('Generating', fill='#', suffix='%(percent)d%% - %(elapsed_td)s', max=total)

        fake = Faker()
        for i in range(total):

            line = DataGenerator.get_fake_data(fake)

            progress_bar.next()
            bulk_lines.append(line)
            if outfile is None:
                result.append(line)

            if len(bulk_lines) == bulk_size:
                outfile_writer.writerows(bulk_lines)
                log.debug(bulk_lines)
                bulk_lines = []

        # write the rest
        if len(bulk_lines) > 0:
            if outfile is not None:
                outfile_writer.writerows(bulk_lines)
                log.debug(bulk_lines)
        progress_bar.finish()

        return result
