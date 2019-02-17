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

    # For executing the celery generator you will need to do the following:
    # 1. workon python-generator
    # 2. docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3
    # 3. celery -A project.lib.celery_app:app  worker --loglevel=debug
    # 4. python -m project.lib.receive
    # 5. python project/lib/main_command.py ce -o '12.csv' -r 11 -b 2 --verbose

    def __init__(self):
        pass

    @staticmethod
    def generate_leads_file(total, bulk_size):
        print('Generating %s leads.' % total)

        print('')

        # start the rabbit consumer
        # print "tasks started"
        # Observable.from_(range(0)).flat_map(
        #     lambda s: executor.submit(receive_messages, s)
        # )
        # start_consuming()
        # print "tasks started"
        bulks = Utils.get_bulks(bulk_size, total)
        # print "tasks started"
        # invoke celery tasks publish to kafka results
        for bulk in bulks:
            generate_task.delay(bulk)

        print "tasks started"
