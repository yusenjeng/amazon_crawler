import sys
import time
import uuid

from pymongo import MongoClient, DESCENDING, HASHED, TEXT, GEO2D
from pymongo.errors import OperationFailure, DuplicateKeyError


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
        self.budget = self.db.budget
        self.createIndex()

    def createIndex(self):
        try:
            self.ad.create_index('adId', unique=True)
            self.budget.create_index('campaignId', unique=True)
            print(' [M] Create indices on collection ads.')
        except OperationFailure as err:
            print(' [M] Write error: {0}'.format(err))

    def insertAd(self, doc):
        try:
            id = self.ad.insert_one(doc).inserted_id
            print(' [M] Insert an AD with _id=', id)
        except DuplicateKeyError as err:
            print(' [M] Insert error: {0}'.format(err))

    def insertBudget(self, doc):
        try:
            id = self.budget.insert_one(doc).inserted_id
            print(' [M] Insert a Budget with _id=', id)
        except DuplicateKeyError as err:
            print(' [M] Insert error: {0}'.format(err))

    def updateBudget(self, doc):
        self.budget.find_one_and_update(
            {'campaignId': doc['campaignId']},
            {'$set': {'budget': doc['budget']} }
        )

    def findAllAds(self, callback):
        opt = {}
        for doc in self.ad.find(opt):
            callback(doc)

    def findOneAd(self, opt):
        return self.ad.find_one(opt)

    def findOneBudget(self, opt):
        return self.budget.find_one(opt)

    def countAds(self):
        return self.ad.count()

    def deleteAll(self):
        # Delete everything in the tweets
        deleted_count = self.ad.delete_many({}).deleted_count
        print(' [M] Delete', deleted_count, 'ads.')
        deleted_count = self.budget.delete_many({}).deleted_count
        print(' [M] Delete', deleted_count, 'budgets.')


if __name__ == '__main__':
    db = AdDB()
    db.connect()

    # CLI for the database management
    if 'delete' in sys.argv:
        db.deleteAll()
    elif 'index' in sys.argv:
        db.createIndex()
    elif 'test' in sys.argv:
        doc = AD()
        db.insertAd(doc)
    elif 'find' in sys.argv:
        pass
