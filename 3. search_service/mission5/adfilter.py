

class Filter():
    def __init__(self, *args, **kwargs):
        self.TH_NUM_ADS = 4
        self.TH_CLICK = 0.0
        self.TH_RELEVANCE = 0.01
        self.TH_PRICE = 0.0
        self.TH_MAIN_LINE_PRICE = 4.5
        return

    # Select by threadholds
    def level0(self, ads):
        if len(ads) < self.TH_NUM_ADS:
            return ads

        filtered = [ad for ad in ads if ad['relevanceScore'] > self.TH_RELEVANCE and ad['pClick'] >= self.TH_CLICK]
        return filtered

    # Select Top k ads
    def level1(self, ads, k=20):
        if len(ads) < self.TH_NUM_ADS:
            return ads

        def key(x):
            return x['relevanceScore'] 
        ads = sorted(ads, key=key, reverse=True)
        return ads[:k]
