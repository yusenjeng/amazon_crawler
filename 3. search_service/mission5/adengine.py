import sys
import json
import cache
import adfilter
import database
import queryparser

class AdEngine():
    def __init__(self):
        self.ads = []
        self.parser = queryparser.NLPParser()
        self.filter = adfilter.Filter()
        
        self.cache = cache.AdCache()
        self.cache.connect()

        self.db = database.AdDB()
        self.db.connect()

    def buildInvertIndex(self):
        print(' [A] loading Ads from DB...')
        print(' [A] building invert indexes...')
        num = self.db.countAds()
        self.db.findAllAds(self.cache.buildInvertIndex)
        print(' [A] found %s ads.' % num)

    def loadAdsFileToDB(self, fn='data/ads.txt', fnBudget='data/budget.txt'):
        self.db.createIndex()

        print(' [A] loading Ads from file...')
        ads = []
        with open(fn) as f:
            content = f.readlines()
            for c in content:
                ads.append(json.loads(c))
        f.close()

        print(' [A] dumping Ads to database...')
        for ad in ads:
            self.db.insertAd(ad)
        
        print(' [A] loading budgets from file...')
        budgets = []
        with open(fnBudget) as f:
            content = f.readlines()
            for c in content:
                budgets.append(json.loads(c))
        f.close()

        print(' [A] dumping budgets to database...')
        for b in budgets:
            self.db.insertBudget(b)

        self.buildInvertIndex()
        print(' [A] done')
    
    def collectAds(self, terms):
        # collect possible Ads
        possibleIds = []
        for term in terms:
            s = self.cache.get(term)
            if not s:
                continue
            possibleIds = possibleIds + json.loads(s)
        # print(' [A] Got %s ads' % len(possibleIds))
        
        # count each matched id
        matchedIds = {}
        for id in possibleIds:
            if id in matchedIds:
                matchedIds[id] += 1
            else:
                matchedIds[id] = 1

        # calculate relevanceScore and 
        collected = []
        for id in matchedIds:
            ad = self.db.findOneAd({'adId':id})
            ad['relevanceScore'] = matchedIds[id] / len(ad['keywords'])
            collected.append(ad)
            # print(' [A] adID=%s relevanceScore=%s' % (id, ad['relevanceScore']))
        return collected
    
    def dedupe(self, ads):
        campaign = set()
        deduped = []
        for ad in ads:
            if ad['campaignId'] in campaign:
                continue
            campaign.add(ad['campaignId'])
            deduped.append(ad)
        return deduped

    def applyBudget(self, ads):
        valid = []
        for ad in ads:
            campaignId = ad['campaignId']
            doc = self.db.findOneBudget({'campaignId':campaignId})

            if (ad['costPerClick'] <= doc['budget'] and ad['costPerClick'] >= self.filter.TH_PRICE):
                # print(' [A] campaignId %s: %s=>%s' % (campaignId, doc['budget'], doc['budget']-ad['costPerClick'] ))
                doc['budget'] -= ad['costPerClick']
                self.db.updateBudget(doc)
                valid.append(ad)
        return valid
    
    def allocate(self, ads):
        for ad in ads:
            if ad['costPerClick'] > self.filter.TH_MAIN_LINE_PRICE:
                ad['position'] = 1
            else:
                ad['position'] = 2
        return ads

    def selectAds(self, query):
        ads = []
        terms = self.parser.understand(query)
        collectedAds = self.collectAds(terms)  # use db & cache
        filteredAds = self.filter.level0(collectedAds)
        filteredAds = self.filter.level1(filteredAds, 20)
        dedupedAds = self.dedupe(filteredAds) 
        ads = self.applyBudget(dedupedAds)
        ads = self.allocate(ads)
        return ads


if __name__ == '__main__':
    engine = AdEngine()

    if 'init' in sys.argv:
        engine.loadAdsFileToDB()
    else:
        ads = engine.selectAds('kid toddler')

        for ad in ads:
            print('adId=%s campaignId=%s position=%s costPerClick=%s relevance=%s' % (ad['adId'], ad['campaignId'], ad['position'], ad['costPerClick'], ad['relevanceScore']))

