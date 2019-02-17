import csv
import logging
import time

from progress.bar import Bar

from project.lib.data_generator import DataGenerator
from project.lib.utils import Utils

log = logging.getLogger("QueueListener")


class QueueListener:
    def __init__(self):
        pass


def listen(queue, file_path, total):
    """listens for messages on the q, writes to file. """

    try:
        progress_bar = Bar('Generating', fill='#', suffix='%(percent)d%% - %(elapsed_td)s', max=total)

        log.debug("Opened file %s: " % file_path)
        outfile = open(file_path, 'w+')

        outfile_writer = csv.writer(outfile, delimiter=',')

        outfile_writer.writerow(DataGenerator.get_header())

        start_time = time.time()

        while 1:
            bulk_lines = queue.get()
            if bulk_lines == 'kill':
                break

            outfile_writer.writerows(bulk_lines)
            progress_bar.next(len(bulk_lines))
            log.debug('bulk write: %s' % bulk_lines)

        elapsed_time = time.time() - start_time
        log.debug("Elapsed %s" % time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        log.debug('Stopping listener')
        Utils.close_file(outfile, progress_bar)

    except (OSError, IOError):
        Utils.error_print('Path is invalid: %s' % file_path)
        log.error("Failed to open file {}:".format(file_path))
        return None
