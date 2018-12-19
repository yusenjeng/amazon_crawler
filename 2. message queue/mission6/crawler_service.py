import sys
import data
import json
import pika
import time
import random
import crawler
import asyncio
import datetime


class CrawlerService():
    def __init__(self):
        self.EXCHANGE_NAME = 'e_crawler'
        self.IN_QUEUE_NAME = 'q_feeds'
        self.OUT_QUEUE_NAME = 'q_ads'
        self.ERR_QUEUE_NAME = 'q_error'
        self.conn = None
        self.ch = None
        self.initQueue()

    def initQueue(self, host='localhost'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.ch = self.conn.channel()

        self.ch.exchange_declare(exchange=self.EXCHANGE_NAME,
                                 exchange_type='direct', durable=True)
        self.ch.queue_declare(queue=self.IN_QUEUE_NAME, durable=True)
        self.ch.queue_declare(queue=self.OUT_QUEUE_NAME, durable=True)
        self.ch.queue_declare(queue=self.ERR_QUEUE_NAME, durable=True)

        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.IN_QUEUE_NAME,
                           routing_key=self.IN_QUEUE_NAME)
        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.OUT_QUEUE_NAME,
                           routing_key=self.OUT_QUEUE_NAME)
        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.ERR_QUEUE_NAME,
                           routing_key=self.ERR_QUEUE_NAME)

    def callback(self, ch, method, properties, body):
        query = json.loads(body)
        print(' [x] Received: campaignId=%s' % (query['campaignId']))

        amazon = crawler.AmazonCrawler()

        try:
            tasks = []
            for page in range(1, 10):
                task = amazon.getAds(query, page)
                tasks.append(task)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.gather(*tasks))
        except:
            msg = 'Refused by Amazon at %s' % datetime.datetime.now.isoformat()
            print(' [*]', msg)
            amazon.sendError(msg)
            time.sleep(60*3)
            return

        time.sleep(3)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.ch.basic_qos(prefetch_count=1)
        self.ch.basic_consume(self.callback, queue=self.IN_QUEUE_NAME)
        self.ch.start_consuming()


if __name__ == '__main__':
    service = CrawlerService()
    while True:
        try:
            service.run()
        except pika.exceptions.ConnectionClosed as err:
            print(' [*] restart consuming...')
            continue
