from __future__ import print_function

import csv
import logging
import multiprocessing as mp
import os
import re
import sys
from threading import current_thread

import cmdln
from concurrent.futures import ProcessPoolExecutor
from faker import Faker
from progress.bar import Bar
from rx import Observable
from rx import config

# from progress_bar import ProgressBar

logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
log = logging.getLogger("CsvRxGenerator")
RE_INT = re.compile(r'^([1-9]\d*|0)$')

fake = Faker()
executor = ProcessPoolExecutor(mp.cpu_count() + 2)

config["concurrency"] = mp


class CsvRxGenerator(cmdln.Cmdln):
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
            error_print('Path is missing or invalid')
            return None

        if not RE_INT.match(opts.rows):
            error_print('Number of rows is invalid')
            return None
        if not RE_INT.match(opts.bulk):
            error_print('Number of bulk is invalid')
            return None

        file_path = opts.output
        total = int(opts.rows)
        bulk = opts.bulk
        try:
            outfile = open(file_path, 'w+')
            log.debug("Opened file %s: " % outfile.name)
            CsvRxGenerator.generate_leads_file(total, outfile, int(bulk))
        except (OSError, IOError) as e:
            error_print('Path is invalid: %s' % file_path)
            log.error("Failed to open file {}:".format(file_path))
            return None

    @staticmethod
    def generate_leads_file(total, outfile, bulk_size=20000):

        print('Generating %s leads. Output file: %s' % (total, os.path.abspath(outfile.name)))
        outfile_writer = csv.writer(outfile, delimiter=',')

        print('')

        header = ['Email', 'First Name', 'Last Name']

        outfile_writer.writerow(header)

        bulks = CsvRxGenerator.get_bulks(bulk_size, total)

        progress_bar = Bar('Generating', fill='#', suffix='%(percent)d%% - %(elapsed_td)s', max=total)
        Observable.from_(bulks).flat_map(
            lambda s: executor.submit(generate_data, s)
        ).subscribe(on_next=lambda x: handle_result(x, outfile_writer, progress_bar),
                    on_completed=lambda: close_file(outfile, progress_bar),
                    on_error=lambda err: print_thread_close_file("on_error: {}".format(err), outfile, progress_bar))

    @staticmethod
    def get_bulks(bulk_size, total):
        bulks = []
        num_of_itr = (total / bulk_size)
        for i in range(0, num_of_itr):
            bulks.append(bulk_size)
        mod = total % bulk_size
        bulks.append(mod)
        log.debug('bulks: %s' % bulks)
        return bulks


def error_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def print_thread(val):
    log.debug("{}, thread: {}".format(val, current_thread().name))


def handle_result(result, outfile_writer, progress_bar):
    log.debug('result: %s' % result)
    progress_bar.next(len(result))
    outfile_writer.writerows(result)


def close_file(f, progress_bar):
    log.debug('closing file %s' % f.name)
    f.close()
    progress_bar.finish()


def print_thread_close_file(err, f, progress_bar):
    log.error("{}, thread: {}".format(err, current_thread().name))
    close_file(f, progress_bar)


def generate_data(bulk):
    log.debug('long time task begins')

    result = []
    for _ in range(bulk):
        first = str(fake.first_name())
        last = str(fake.last_name())
        email = str(fake.email())

        line = [email, first, last]
        result.append(line)
    log.debug('long time task finished %s' % result)

    return result


def main():
    csv_generator = CsvRxGenerator()
    sys.exit(csv_generator.main())


if __name__ == "__main__":
    main()
