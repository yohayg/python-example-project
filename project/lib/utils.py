from __future__ import print_function

import logging
import sys

log = logging.getLogger("CsvRxGenerator")


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def error_print(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def get_bulks(bulk_size, total):
        bulks = []
        num_of_itr = (total / bulk_size)
        for i in range(0, num_of_itr):
            bulks.append(bulk_size)
        mod = total % bulk_size
        if mod > 0:
            bulks.append(mod)
        log.debug('bulks: %s' % bulks)
        return bulks

    @staticmethod
    def close_file(f, progress_bar):
        log.debug('closing file %s' % f.name)
        f.close()
        progress_bar.finish()
