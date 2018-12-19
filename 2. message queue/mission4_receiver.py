import sys
import pika
import time
import datetime

conn = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
ch = conn.channel()

exchange_name = 'e_topic_logs'
ch.queue_declare(queue='q_warning_1', durable=True)
ch.queue_declare(queue='q_warning_2', durable=True)


def callback(ch, method, properties, body):
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(' [x] DONE %s from %s' % (body, method.routing_key))


print(' [*] Waiting for messages.')
ch.basic_qos(prefetch_count=1)
ch.basic_consume(callback, queue='q_warning_1')
ch.basic_consume(callback, queue='q_warning_2')
ch.start_consuming()
