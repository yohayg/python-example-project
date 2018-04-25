import csv
import logging
import multiprocessing as mp
import os
from threading import current_thread

from concurrent.futures import ProcessPoolExecutor
from progress.bar import Bar
from rx import Observable
from rx import config

from project.lib.data_generator import DataGenerator, generate_data
from project.lib.utils import Utils

log = logging.getLogger("CsvRxGenerator")

executor = ProcessPoolExecutor(mp.cpu_count() + 2)

config["concurrency"] = mp


class CsvRxGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_leads_file(total, outfile, bulk_size=20000):
        print('Generating %s leads. Output file: %s' % (total, os.path.abspath(outfile.name)))
        outfile_writer = csv.writer(outfile, delimiter=',')

        print('')

        outfile_writer.writerow(DataGenerator.get_header())

        bulks = Utils.get_bulks(bulk_size, total)

        progress_bar = Bar('Generating', fill='#', suffix='%(percent)d%% - %(elapsed_td)s', max=total)
        Observable.from_(bulks).flat_map(
            lambda s: executor.submit(generate_data, s, 1)
        ).subscribe(on_next=lambda x: handle_result(x, outfile_writer, progress_bar),
                    on_completed=lambda: Utils.close_file(outfile, progress_bar),
                    on_error=lambda err: print_thread_close_file("on_error: {}".format(err), outfile, progress_bar))


def print_thread(val):
    log.debug("{}, thread: {}".format(val, current_thread().name))


def handle_result(result, outfile_writer, progress_bar):
    log.debug('result: %s' % result)
    progress_bar.next(len(result))
    outfile_writer.writerows(result)


def print_thread_close_file(err, f, progress_bar):
    log.error("{}, thread: {}".format(err, current_thread().name))
    Utils.close_file(f, progress_bar)
