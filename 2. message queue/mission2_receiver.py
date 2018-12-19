import sys
import pika
import time
import datetime

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create if needed
channel.queue_declare(queue='q_rocket_5', durable=True)
print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    print(' [x] Received %s' % body)
    time.sleep(2)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(' [x] Done')


# No more than 1 msg at a time
# Dispatch new msg to other worker
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='q_rocket_5')

channel.start_consuming()
