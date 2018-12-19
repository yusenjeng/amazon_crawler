import sys
import pika
import time
import datetime

conn = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = conn.channel()

exchange_name = 'cs502_1802_ex'
queue_name_warning = 'q_rocket_warning'
queue_name_error = 'q_rocket_error'


def callback(ch, method, properties, body):
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(' [x] DONE %s' % body)


if sys.argv[1] == 'warning':
    queue_name = queue_name_warning
else:
    queue_name = queue_name_error


print(' [*] Waiting for messages.')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue=queue_name)
channel.start_consuming()
