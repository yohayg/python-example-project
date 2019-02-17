import json
import logging

import pika

from project.lib.celery_app import app
from project.lib.data_generator import generate_data

log = logging.getLogger("CsvMpGenerator")


@app.task(ignore_result=False)
def generate_task(bulk):
    log.debug('long time task begins')

    result = generate_data(bulk, None)

    print result

    print("%s" % result)
    log.debug("putting in queue args: %s result: %s" % (bulk, result))
    parameters = pika.ConnectionParameters('localhost', 5672, '/')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='data_queue')

    channel.basic_publish(exchange='', routing_key='data_queue', body=json.dumps({'results': result}))
    log.debug('long time task finished')
    connection.close()
