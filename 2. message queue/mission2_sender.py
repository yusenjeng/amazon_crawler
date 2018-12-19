import sys
import pika
import datetime

conn = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = conn.channel()

channel.queue_declare(queue='q_rocket_5', durable=True)

msg = 'Hello! ' + str(datetime.datetime.now())
channel.basic_publish(exchange='',
                      routing_key='q_rocket_5',
                      body=msg,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # make message persistent
                          #   delivery_mode=1, # non-persistent
                      ))
print(" [x] Sent %s" % msg)
conn.close()
