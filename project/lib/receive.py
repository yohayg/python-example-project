import csv
import json

import pika
from project.lib.data_generator import DataGenerator

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='data_queue')
total = 11
bulk = 2
count = 0
outfile = open('test.csv', 'w+')
outfile_writer = csv.writer(outfile, delimiter=',')


outfile_writer.writerow(DataGenerator.get_header())


def callback(ch, method, properties, body):

    json_loads = json.loads(body)
    #
    global count
    count = count + 1
    print("%d %d" % (count, total))
    results = json_loads['results']
    print(" [x] Received %r" % results)
    # print(" [x] Received %r" % results)
    outfile_writer.writerows(results)
    if (count * bulk) >= total:
        print('done')
        outfile.close()
        connection.close()


def test():
    channel.basic_consume(callback,
                          queue='data_queue',
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


if __name__ == '__main__':
    test()
