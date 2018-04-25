import csv
import json

import pika

# docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3
parameters = pika.ConnectionParameters('localhost', 5672, '/')

queue_name = 'data_queue'

total = 11
bulk = 2
count = 0
outfile = open('test.csv', 'w+')
outfile_writer = csv.writer(outfile, delimiter=',')


class RabbitMqListener:

    def __init__(self):
        pass

    @staticmethod
    def get_connection():
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        return connection

    def start_consuming(self):
        channel = self.get_connection().channel()
        channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)

        print(' [*] Waiting for messages')

        channel.start_consuming()

        print(' [*] Waiting for messages')


def callback(ch, method, properties, body):
    json_loads = json.loads(body)

    global count
    count = count + 1
    print("%d %d" % (count, total))
    results = json_loads['results']
    print(" [x] Received %r" % results)
    outfile_writer.writerows(results)
    if (count * bulk) >= total:
        print('done')
        outfile.close()
        channel.stop_consuming()
        connection.close()


if __name__ == '__main__':
    start_consuming()
