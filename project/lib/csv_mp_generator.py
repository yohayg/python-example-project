import logging
import multiprocessing as mp

from project.lib.data_generator import generate_data
from project.lib.queue_listener import listen
from project.lib.utils import Utils

logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
log = logging.getLogger("CsvMpGenerator")


class CsvMpGenerator:

    def __init__(self):
        pass

    @staticmethod
    def generate_leads_file(total, file_path, bulk_size=20000):

        print('Generating %s leads. Output file: %s' % (total, file_path))

        print('')

        bulks = Utils.get_bulks(bulk_size, total)

        manager = mp.Manager()
        q = manager.Queue()
        pool = mp.Pool(mp.cpu_count() + 2)

        pool.apply_async(listen, (q, file_path, total))

        jobs = []
        for index, bulk in enumerate(bulks):
            job = pool.apply_async(bulk_data_queue, (bulk, q, index))
            jobs.append(job)

        # collect results from the workers through the pool result queue
        for job in jobs:
            job.get()

        # now we are done, kill the listener
        q.put('kill')
        pool.close()


def bulk_data_queue(bulk, queue, index):
    log.debug('long time task begins')

    result = generate_data(bulk, index)

    log.debug("putting in queue args: %s result: %s" % (bulk, result))

    queue.put(result)
    log.debug('long time task finished')

    return result
