import time
import aiohttp
import asyncio
import utility
from bs4 import BeautifulSoup
from random import randint


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


class ProxyCrawler():
    def __init__(self):
        self.proxyhost = '199.101.97.183'  # default proxy server
        self.proxyport = '60099'  # default proxy port
        self.account = 'bittiger'
        self.passwd = 'cs504'
        pass

    def setAuth(self, account, passwd):
        self.account = account
        self.passwd = passwd

    def setProxy(self, host, port):
        self.proxyhost = host
        self.proxyport = str(port)

    def setUrl(self, url):
        self.url = url

    def parse(self, html, url, opt):
        pass

    def onFinish(self, results):
        pass

    def makeProxyUrl(self):
        # proxy = 'http://bittiger:cs504@199.101.97.183:60099'
        return 'http://'+self.account+':' + self.passwd + \
            '@' + self.proxyhost+':'+self.proxyport

    async def fetch(self, session, url):
        proxy = self.makeProxyUrl()
        async with session.get(url, proxy=proxy, ssl=False) as res:
            return await res.text()

    async def run(self, opt):
        print('Start crawling', opt['url'])
        async with aiohttp.ClientSession(headers=opt['headers']) as session:
            html = await self.fetch(session, opt['url'])
            results = self.parse(html, opt)
            self.onFinish(results)


class AmazonCrawler(ProxyCrawler):
    def __init__(self, fnQuery='query.txt', fnOutput='output.txt', fnProxy='proxy.csv', fnLog='log.txt'):
        super().__init__()
        self.PATH_CONFIG = './config/'
        self.queries = []
        self.proxies = []
        self.visitedUrl = set()

        self.loadQuery(fnQuery)
        self.loadProxy(fnProxy)
        self.initOutput(fnOutput)
        self.initLogger(fnLog)
        return

    def onFinish(self, results):
        log = utility.LogJSON(self.fnOutput, 'a')
        for r in results:
            log.write(r)
        log.close()

    def parse(self, html, opt):
        soup = BeautifulSoup(html, 'html.parser')

        category = soup.find(
            'h4', class_='a-size-small a-spacing-top-mini a-color-base a-text-bold')
        if not category:
            category = ''
        else:
            category = category.string

        items = soup.find_all(utility.hasAsin)

        # if len(items) < 1:
        #     self.logger.write('0 result for query :' + opt['url'] +
        #                       ', page = ' + opt['page'])

        # print(opt)
        print('Num of items:', len(items))

        products = []
        for item in items:
            ad = AD()

            ad['query'] = opt['query']
            ad['bidPrice'] = opt['bidPrice']
            ad['campaignId'] = opt['campaignId']
            ad['query_group_id'] = opt['query_group_id']
            ad['category'] = category

            try:
                self.parseProductLink(item, ad)
                self.parseProductTitle(item, ad)
                self.parseProductThumbnail(item, ad)
                self.parseProductKeywords(item, ad)
                self.parseProductBrand(item, ad)
                self.parseProductPrice(item, ad)
            except utility.CrawlerError as err:
                # if err.code != 0:
                #     print(err)
                continue

            products.append(ad)
        return products

    def parseProductLink(self, item, ad):
        href = item.find(
            'a', class_='a-link-normal a-text-normal')
        if not href:
            raise utility.CrawlerError('Product format not correct', 0)

        href = href.get('href')
        href = utility.normalizeUrl(href)
        ad['detail_url'] = href

        if href in self.visitedUrl:
            raise utility.CrawlerError('Product link already exists')
        else:
            self.visitedUrl.add(href)

    def parseProductTitle(self, item, ad):
        title = item.find('h2')
        if not title:
            raise utility.CrawlerError('Product title is missing')

        if title.get('data-attribute') is None:
            raise utility.CrawlerError('Product title is missing')

        ad['title'] = title['data-attribute']

    def parseProductThumbnail(self, item, ad):
        thumbnail = item.find('img').get('src')
        ad['thumbnail'] = thumbnail

    def parseProductKeywords(self, item, ad):
        ad['keywords'] = utility.cleanedTokenize(ad['title'])
        if len(ad['keywords']) < 1:
            raise utility.CrawlerError('Lack of keywords')

    def parseProductBrand(self, item, ad):
        brand = item.find_all(
            'span', class_='a-size-small a-color-secondary')

        if len(brand) < 1:
            raise utility.CrawlerError('Product brand is missing')
        brand = brand[1].string
        ad['brand'] = brand

    def parseProductPrice(self, item, ad):
        whole = item.find(class_='sx-price-whole')
        fraction = item.find(class_='sx-price-fractional')
        if whole is None or fraction is None:
            ad['price'] = None
        else:
            whole = whole.string.replace(',', '')
            fraction = fraction.string
            ad['price'] = float(whole + '.' + fraction)

        product_id = item.get('data-asin')
        ad['adId'] = product_id

    def getAdsByQuery(self, idx, page=0):
        self.switchProxy()

        ad = self.queries[idx]
        opt = {}
        opt['url'] = self.makeQueryUrl(ad['query'], page)
        opt['headers'] = self.makeHeaders('mac')
        opt['page'] = page
        opt['query'] = ad['query']
        opt['bidPrice'] = ad['bidPrice']
        opt['campaignId'] = ad['campaignId']
        opt['query_group_id'] = ad['query_group_id']

        return self.run(opt)

    def makeHeaders(self, device):
        USER_AGENT_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
        USER_AGENT_IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"

        AGENT = USER_AGENT_MAC if device == 'mac' else USER_AGENT_IPHONE

        headers = {
            'User-Agent': AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8'
        }
        return headers

    def makeQueryUrl(self, target, page=0):
        url = 'https://www.amazon.com/s/ref=nb_sb_noss?field-keywords=' + target
        if page > 1:
            url = url + "&page=" + str(page)
        return url

    def switchProxy(self):
        idx = randint(0, len(self.proxies)-1)
        proxy = self.proxies[idx]
        self.setProxy(proxy[0], proxy[1])
        self.setAuth(proxy[3], proxy[4])

    def loadProxy(self, fnProxy):
        with open(self.PATH_CONFIG+fnProxy) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = [x.split(',') for x in content]
        for c in content:
            if len(c) < 4 or c[0] == '':
                continue
            c[1] = int(c[1])
            c[2] = int(c[2])
            self.proxies.append(c)

    def loadQuery(self, fnQuery):
        with open(self.PATH_CONFIG+fnQuery) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
        content = [x.split(',') for x in content]

        for c in content:
            if len(c) < 4 or c[0] == '':
                continue
            ad = AD()
            ad['query'] = c[0].strip()
            ad['bidPrice'] = float(c[1].strip())
            ad['campaignId'] = int(c[2].strip())
            ad['query_group_id'] = int(c[3].strip())
            self.queries.append(ad)

    def initOutput(self, fnOutput):
        self.fnOutput = fnOutput
        log = utility.LogJSON(fnOutput, 'w')
        log.close()

    def initLogger(self, fnLog):
        self.fnLog = fnLog
        log = utility.Log(fnLog, 'w')
        log.close()

    def numQueries(self):
        return len(self.queries)


class CrawlerManager():
    def __init__(self, crawler):
        self.crawler = crawler

    def runQuery(self, n):
        num = self.crawler.numQueries()
        if n < 0 and n >= num:
            return

        tasks = []
        for page in range(1, 5):
            task = self.crawler.getAdsByQuery(n, page)

            tasks.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))

    def runAllQueries(self, start=0):
        num = self.crawler.numQueries()

        for q in range(start, num):
            print('Start query #', q)
            self.runQuery(q)
            time.sleep(5)


if __name__ == '__main__':
    crawler = AmazonCrawler()
    manager = CrawlerManager(crawler)

    # manager.runQuery(10)
    manager.runAllQueries()
