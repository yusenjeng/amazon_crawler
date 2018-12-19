import sys
import time
import uuid

from pymongo import MongoClient, DESCENDING, HASHED, TEXT, GEO2D
from pymongo.errors import OperationFailure, DuplicateKeyError


def AD():
    ret = {}
    ret['adId'] = str(uuid.uuid4())
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


class AdDB(object):
    def __init__(self, dbname='CS502'):
        self.MONGO_ADDRESS = 'localhost'
        self.MONGO_PORT = 27017
        self.MONGO_USER = ''
        self.MONGO_PASSWD = ''
        self.db = None
        self.dbname = dbname

    def connect(self):
        # Connect to remote mongodb and keep the ad collection
        client = MongoClient(self.MONGO_ADDRESS, self.MONGO_PORT)
        self.db = client[self.dbname]
        # self.db.authenticate(self.MONGO_USER, self.MONGO_PASSWD)
        self.ad = self.db.ad

    def createIndex(self, hours=1):
        try:
            self.ad.create_index('adId', unique=True)
            self.ad.create_index([('campaignId', DESCENDING)])
            self.ad.create_index([('created_at', DESCENDING)])
            print(' [M] Create indices on collection ads.')
        except OperationFailure as err:
            print(' [M] Write error: {0}'.format(err))

    def insertAd(self, doc):
        try:
            id = self.ad.insert_one(doc).inserted_id
            print(' [M] Insert an AD with _id=', id)
        except DuplicateKeyError as err:
            print(' [M] Insert error: {0}'.format(err))

    # def findAds(self, keyword):

    #     # Merge query parameters into the dict
    #     opt = {}

    #     if keyword is not None:
    #         opt['$text'] = {'$search': keyword}

    #     # sort = [('created_at', DESCENDING)]
    #     sort = []

    #     # Fetch the most recent 100 tweets
    #     results = self.tweets.find(opt, sort=sort).limit(100)

    #     print(' [M] Query operators:', opt)

    def deleteAllAds(self):
        # Delete everything in the tweets
        deleted_count = self.ad.delete_many({}).deleted_count
        print(' [M] Delete', deleted_count, 'ads.')


if __name__ == '__main__':
    db = AdDB()
    db.connect()

    # CLI for the database management
    if 'delete' in sys.argv:
        db.deleteAllAds()
    elif 'index' in sys.argv:
        db.createIndex()
    elif 'test' in sys.argv:
        doc = AD()
        db.insertAd(doc)
