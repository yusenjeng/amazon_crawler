import sys
import pika
import datetime

conn = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = conn.channel()

exchange_name = 'cs502_1802_ex'
queue_name_warning = 'q_rocket_warning'
queue_name_error = 'q_rocket_error'

channel.exchange_declare(exchange=exchange_name,
                         exchange_type='direct', durable=True)
channel.queue_declare(queue=queue_name_warning, durable=True)
channel.queue_declare(queue=queue_name_error, durable=True)

channel.queue_bind(exchange=exchange_name,
                   queue=queue_name_warning,
                   routing_key=queue_name_warning)

channel.queue_bind(exchange=exchange_name,
                   queue=queue_name_error,
                   routing_key=queue_name_error)


for i in range(10):
    msg = ''
    routing_key = ''

    if i % 2 == 0:
        msg = 'Warning: ' + str(datetime.datetime.now())
        routing_key = queue_name_warning
    else:
        msg = 'Error: ' + str(datetime.datetime.now())
        routing_key = queue_name_error

    print(' [x] Send to %s: %s' % (routing_key, msg))
    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=msg,
                          properties=pika.BasicProperties(
                              delivery_mode=2
                          ))

conn.close()
