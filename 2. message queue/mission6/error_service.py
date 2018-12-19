import sys
import data
import json
import pika
import time
import random
import crawler
import asyncio
import utility
import datetime


class ErrorService():
    def __init__(self, fnError):
        self.EXCHANGE_NAME = 'e_crawler'
        self.ERR_QUEUE_NAME = 'q_error'
        self.conn = None
        self.ch = None
        self.initErrorLogger(fnError)
        self.initQueue()

    def initErrorLogger(self, fn):
        self.fn = fn
        log = utility.Log(fn, 'w')
        log.close()

    def initQueue(self, host='localhost'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.ch = self.conn.channel()

        self.ch.exchange_declare(exchange=self.EXCHANGE_NAME,
                                 exchange_type='direct', durable=True)
        self.ch.queue_declare(queue=self.ERR_QUEUE_NAME, durable=True)

        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.ERR_QUEUE_NAME,
                           routing_key=self.ERR_QUEUE_NAME)

    def callback(self, ch, method, properties, body):
        print(' [x] Received: %s from %s' % (body, method.routing_key))

        log = utility.Log(self.fn, 'a')
        log.write(body)
        log.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.ch.basic_qos(prefetch_count=1)
        self.ch.basic_consume(self.callback, queue=self.ERR_QUEUE_NAME)
        self.ch.start_consuming()


if __name__ == '__main__':
    service = ErrorService('error.txt')
    service.run()
