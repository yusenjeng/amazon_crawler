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
                        exchange_type='topic', durable=True)

    ch.queue_declare(queue='q_warning_1', durable=True)
    ch.queue_declare(queue='q_warning_2', durable=True)
    ch.queue_declare(queue='q_error', durable=True)
    ch.queue_declare(queue='q_all', durable=True)

    ch.queue_bind(exchange=exchangename,
                  queue='q_warning_1',
                  routing_key='#.warn')

    ch.queue_bind(exchange=exchangename,
                  queue='q_warning_2',
                  routing_key='#.warn.*')
    ch.queue_bind(exchange=exchangename,
                  queue='q_error',
                  routing_key='*.error')
    ch.queue_bind(exchange=exchangename,
                  queue='q_all',
                  routing_key='*.*')
    return conn, ch


exchange_name = 'e_topic_logs'
host_name = 'localhost'
conn, ch = init(host_name, exchange_name)


for i in range(10):
    msg = ''
    routing_key = ''
    num = random.randint(1, 100)

    if i % 3 == 0:
        msg = 'Warning: ' + str(datetime.datetime.now())
        routing_key = str(num)+'.warn'
    elif i % 3 == 1:
        msg = 'Warning: ' + str(datetime.datetime.now())
        routing_key = str(num)+'.warn.'+str(random.randint(1, 100))
    else:
        msg = 'Error: ' + str(datetime.datetime.now())
        routing_key = str(num)+'.error'

    print(' [x] Send to %s: %s' % (routing_key, msg))
    ch.basic_publish(exchange=exchange_name,
                     routing_key=routing_key,
                     body=msg,
                     properties=pika.BasicProperties(
                         delivery_mode=2
                     ))

conn.close()
