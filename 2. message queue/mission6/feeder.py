import sys
import data
import json
import pika
import time
import random
import datetime


class Feeder():
    def __init__(self, fnQuery='query.txt'):
        self.PATH_CONFIG = './config/'
        self.queries = []

        self.EXCHANGE_NAME = 'e_crawler'
        self.IN_QUEUE_NAME = 'q_feeds'
        self.OUT_QUEUE_NAME = 'q_product'
        self.ERR_QUEUE_NAME = 'q_error'
        self.conn = None
        self.ch = None
        self.initQueue()

    def loadQuery(self, fnQuery):
        self.queries = []

        with open(self.PATH_CONFIG+fnQuery) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = [x.split(',') for x in content]

        for c in content:
            if len(c) < 4 or c[0] == '':
                continue
            ad = data.AD()
            ad['query'] = c[0].strip()
            ad['bidPrice'] = float(c[1].strip())
            ad['campaignId'] = int(c[2].strip())
            ad['query_group_id'] = int(c[3].strip())
            self.queries.append(ad)

    def initQueue(self, host='localhost'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.ch = self.conn.channel()

        self.ch.exchange_declare(exchange=self.EXCHANGE_NAME,
                                 exchange_type='direct', durable=True)
        self.ch.queue_declare(queue=self.IN_QUEUE_NAME, durable=True)
        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.IN_QUEUE_NAME,
                           routing_key=self.IN_QUEUE_NAME)

    def send(self, msg=''):
        self.ch.basic_publish(exchange=self.EXCHANGE_NAME,
                              routing_key=self.IN_QUEUE_NAME,
                              body=msg,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))

    def run(self, fnQuery='query.txt'):
        self.loadQuery(fnQuery)
        for q in self.queries:
            msg = json.dumps(q)
            self.send(msg)


if __name__ == '__main__':
    feeder = Feeder('query.txt')
    feeder.run()
