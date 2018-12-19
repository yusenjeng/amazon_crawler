import sys
import pika


def client1():
    conn = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = conn.channel()

    channel.basic_publish(exchange='cs502_1802_ex',
                          #   routing_key='q_rocket_1',
                          routing_key='',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    conn.close()


def client2():
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)

    conn = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = conn.channel()

    # manual acknowledgement by default
    # We turned off the acknowledgement by setting no_ack=True
    channel.basic_consume(callback,
                          queue='q_rocket_1',
                          no_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    if sys.argv[1] == '1':
        client1()
    else:
        client2()
