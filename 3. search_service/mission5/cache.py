import sys
import data
import json
import time
import uuid
import redis


class AdCache(object):
    def __init__(self, dbname='CS502'):
        self.REDIS_ADDRESS = 'localhost'
        self.REDIS_PORT = 6379

    def connect(self):
        self.cli = redis.Redis(
            host=self.REDIS_ADDRESS, port=self.REDIS_PORT, password='')

    def get(self, key):
        return self.cli.get(key)

    def set(self, key, val):
        self.cli.set(key, val)

    def has(self, key):
        return self.cli.exists(key)

    def delete(self, key):
        self.cli.delete(key)

    def cleanInvertIndex(self):
        for key in self.cli.keys('*'):
            self.delete(key)

    def buildInvertIndex(self, ad):

        keywords = ad['keywords']  # Keywords had been cleanedTokenized

        for i in range(len(keywords)):
            w = keywords[i]
            if self.has(w):
                val = json.loads(self.get(w))
                if ad['adId'] not in val:
                    val.append(ad['adId'])
                    self.set(w, json.dumps(val))
            else:
                val = [ad['adId']]
                self.set(w, json.dumps(val))


if __name__ == '__main__':
    db = AdCache()
    db.connect()

    # db.set('aa', 11)
    # print(db.has('aa'))
    # db.delete('aa')
    # print(db.has('aa'))

    # db.cleanInvertIndex()

    # ad = data.AD()
    # ad['adId'] = 'B017E9NKOC'
    # ad['keywords'] = ["snow", "joe", "ion", "cordless", "single", "stage", "brushless", "snow", "blower", "rechargeable", "ecosharp", "battery"]
    # db.buildInvertIndex(ad)

    # print(db.get('123'))