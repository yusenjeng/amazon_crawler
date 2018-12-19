import sys
import pika
import time
import datetime

conn = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
ch = conn.channel()

exchange_name = 'cs502_1802_ex'
queue_name_warning = 'q_rocket_warning'
queue_name_error = 'q_rocket_error'


def callback(ch, method, properties, body):
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(' [x] DONE %s from %s' % (body, method.routing_key))


print(' [*] Waiting for messages.')
ch.basic_qos(prefetch_count=1)
ch.basic_consume(callback, queue=queue_name_warning)
ch.basic_consume(callback, queue=queue_name_error)
ch.start_consuming()
