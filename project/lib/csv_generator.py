from __future__ import print_function

import csv
import logging
import os
import re
import sys

import cmdln
from faker import Faker
from progress.bar import Bar

# from progress_bar import ProgressBar

logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
log = logging.getLogger("CsvGenerator")
RE_INT = re.compile(r'^([1-9]\d*|0)$')


class CsvGenerator(cmdln.Cmdln):
    name = "csv-gen"

    @cmdln.alias("generate", "g")
    @cmdln.option("-o", "--output", action="store",
                  help="the output file", dest="output")
    @cmdln.option("-r", "--rows", action="store",
                  help="number of generated rows", dest="rows")
    @cmdln.option("-b", "--bulk", action="store",
                  help="bulk size of rows written to file", dest="bulk", default='1000')
    @cmdln.option("-v", "--verbose", action="store_true",
                  help="verbose", dest="verbose")
    def do_generate_leads(self, sub_cmd, opts, *args):
        """${cmd_name}: generates leads csv data

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            log.setLevel(logging.DEBUG)

        log.debug('opts: %s args %s' % (opts, args))
        if opts.output is '':
            eprint('Path is missing or invalid')
            return None

        if not RE_INT.match(opts.rows):
            eprint('Number of rows is invalid')
            return None
        if not RE_INT.match(opts.bulk):
            eprint('Number of bulk is invalid')
            return None

        file_path = opts.output
        total = int(opts.rows)
        bulk = opts.bulk

        try:
            with open(file_path, 'w+') as outfile:
                log.debug("Opened file %s: " % outfile.name)
                return CsvGenerator.generate_leads_file(total, outfile, int(bulk))
        except (OSError, IOError) as e:
            eprint('Path is invalid: %s' % file_path)
            log.debug("Failed to open file %s:" % file_path, e)
            return None

    @staticmethod
    def generate_leads_file(total, outfile, bulk_size=1000):
        fake = Faker()
        # start_time = time.time()

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

        for i in range(total):

            first = str(fake.first_name())
            last = str(fake.last_name())
            email = str(fake.email())

            line = [email, first, last]

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
        # ProgressBar.progress(total, total, status='done')
        progress_bar.finish()

        return result


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    csv_generator = CsvGenerator()
    sys.exit(csv_generator.main())


if __name__ == "__main__":
    main()
