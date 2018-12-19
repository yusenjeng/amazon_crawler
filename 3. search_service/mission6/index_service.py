import sys
import json
import pika
import time
import robot
import random
import asyncio
import datetime


class IndexService():
    def __init__(self, fn):
        self.EXCHANGE_NAME = 'e_crawler'
        self.OUT_QUEUE_NAME = 'q_ads'
        self.conn = None
        self.ch = None
        self.initLogger(fn)
        self.initQueue()

    def initLogger(self, fn):
        self.fn = fn
        log = robot.utility.Log(fn, 'w')
        log.close()

    def initQueue(self, host='localhost'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.ch = self.conn.channel()

        self.ch.exchange_declare(exchange=self.EXCHANGE_NAME,
                                 exchange_type='direct', durable=True)
        self.ch.queue_declare(queue=self.OUT_QUEUE_NAME, durable=True)

        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.OUT_QUEUE_NAME,
                           routing_key=self.OUT_QUEUE_NAME)

    def callback(self, ch, method, properties, body):
        print(' [x] Received: %s from %s' % (body, method.routing_key))

        ad = json.loads(body)
        log = robot.utility.LogJSON(self.fn, 'a')
        log.write(ad)
        log.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.ch.basic_qos(prefetch_count=1)
        self.ch.basic_consume(self.callback, queue=self.OUT_QUEUE_NAME)
        self.ch.start_consuming()


if __name__ == '__main__':
    service = IndexService('ads.txt')
    service.run()
