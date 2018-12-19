import sys
import pika
import time
import random
import datetime


def init(hostname, exchangename):
    conn = pika.BlockingConnection(
        pika.ConnectionParameters(host=hostname))
    ch = conn.channel()

    ch.exchange_declare(exchange=exchangename,
                        exchange_type='fanout', durable=True)

    ch.queue_declare(queue='q_warning_1', durable=True)
    ch.queue_declare(queue='q_warning_2', durable=True)
    ch.queue_declare(queue='q_warning_3', durable=True)
    ch.queue_declare(queue='q_warning_4', durable=True)

    ch.queue_bind(exchange=exchangename,
                  queue='q_warning_1',
                  routing_key='')
    ch.queue_bind(exchange=exchangename,
                  queue='q_warning_2',
                  routing_key='')
    ch.queue_bind(exchange=exchangename,
                  queue='q_warning_3',
                  routing_key='')
    ch.queue_bind(exchange=exchangename,
                  queue='q_warning_4',
                  routing_key='')
    return conn, ch


exchange_name = 'e_fanout_logs'
conn, ch = init('localhost', exchange_name)

for i in range(10):
    msg = 'Hello ' + str(datetime.datetime.now())
    print(' [x] Broadcasting: %s' % (msg))
    ch.basic_publish(exchange=exchange_name,
                     routing_key='',
                     body=msg,
                     properties=pika.BasicProperties(
                         delivery_mode=2
                     ))

conn.close()
