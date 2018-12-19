import sys
import json
import time
import uuid
import redis


def AD():
    ret = {}
    ret['adId'] = 0
    ret['campaignId'] = 0
    ret['keyWords'] = []
    ret['relevanceScore'] = 0
    ret['pClick'] = 0
    ret['bidPrice'] = 0
    ret['rankScore'] = 0
    ret['qualityScore'] = 0
    ret['costPerClick'] = 0
    ret['position'] = 0
    ret['title'] = ''
    ret['price'] = 0
    ret['thumbnail'] = ''
    ret['description'] = ''
    ret['brand'] = ''
    ret['detail_url'] = ''
    ret['query'] = ''
    ret['query_group_id'] = 0
    ret['category'] = ''
    return ret


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

    def delete(self, key):
        self.cli.delete(key)

    def test(self):
        ad = AD()
        print(ad)
        self.set(ad['campaignId'], json.dumps(ad))
        ret = self.get(ad['campaignId'])
        print(ret)
        self.delete(ad['campaignId'])


if __name__ == '__main__':
    db = AdCache()
    db.connect()
    db.test()
