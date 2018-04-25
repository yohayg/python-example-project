import logging
import multiprocessing as mp

from concurrent.futures import ProcessPoolExecutor

# from rx import Observable
from project.lib.celery_tasks import generate_task
# from project.lib.rabbit_mq_listener import receive_messages
from project.lib.utils import Utils

logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
log = logging.getLogger("CsvCeleryGenerator")
executor = ProcessPoolExecutor(mp.cpu_count() + 2)


class CsvCeleryGenerator:

    # 1. celery -A project.lib.celery_app:app  worker --loglevel=debug
    # 2. python project/lib/receive.py
    # 3. python project/lib/main_command.py ce -o '12.csv' -r 11 -b 2 --verbose

    def __init__(self):
        pass

    @staticmethod
    def generate_leads_file(total, file_path, bulk_size=20000):
        print('Generating %s leads. Output file: %s' % (total, file_path))

        print('')

        print('Generating %s leads. Output file: %s' % (total, file_path))

        print('')

        # start the rabbit consumer
        print "tasks started"
        # Observable.from_(range(0)).flat_map(
        #     lambda s: executor.submit(receive_messages, s)
        # )
        # start_consuming()
        print "tasks started"
        bulks = Utils.get_bulks(bulk_size, total)
        print "tasks started"
        # invoke celery tasks publish to kafka results
        for index, bulk in enumerate(bulks):
            generate_task.delay(index, bulk)

        print "tasks started"


def handle_result(async):
    async.wait()
