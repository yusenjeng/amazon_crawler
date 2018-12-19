import json
import pika
import time
import random
import aiohttp
import asyncio
from . import utility
from bs4 import BeautifulSoup
from advertising import data

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
    def __init__(self, fnProxy='proxy.csv'):
        super().__init__()
        self.PATH_CONFIG = 'data/'
        self.queries = []
        self.proxies = []
        self.visitedUrl = set()

        self.loadProxy(fnProxy)

        self.EXCHANGE_NAME = 'e_crawler'
        self.IN_QUEUE_NAME = 'q_feeds'
        self.OUT_QUEUE_NAME = 'q_ads'
        self.ERR_QUEUE_NAME = 'q_error'
        self.conn = None
        self.ch = None
        self.initQueue()
        return

    def initQueue(self, host='localhost'):
        self.conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self.ch = self.conn.channel()

        self.ch.exchange_declare(exchange=self.EXCHANGE_NAME,
                                 exchange_type='direct', durable=True)
        self.ch.queue_declare(queue=self.OUT_QUEUE_NAME, durable=True)
        self.ch.queue_declare(queue=self.ERR_QUEUE_NAME, durable=True)

        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.OUT_QUEUE_NAME,
                           routing_key=self.OUT_QUEUE_NAME)
        self.ch.queue_bind(exchange=self.EXCHANGE_NAME,
                           queue=self.ERR_QUEUE_NAME,
                           routing_key=self.ERR_QUEUE_NAME)

    def sendProduct(self, msg=''):
        self.ch.basic_publish(exchange=self.EXCHANGE_NAME,
                              routing_key=self.OUT_QUEUE_NAME,
                              body=msg,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))

    def sendError(self, msg=''):
        self.ch.basic_publish(exchange=self.EXCHANGE_NAME,
                              routing_key=self.ERR_QUEUE_NAME,
                              body=msg,
                              properties=pika.BasicProperties(
                                  delivery_mode=2
                              ))

    def onFinish(self, results):
        print(' [C] Get', len(results), 'results')
        for r in results:
            msg = json.dumps(r)
            self.sendProduct(msg)

    def parse(self, html, opt):
        soup = BeautifulSoup(html, 'html.parser')

        category = soup.find(
            'h4', class_='a-size-small a-spacing-top-mini a-color-base a-text-bold')
        if not category:
            category = ''
        else:
            category = category.string

        items = soup.find_all(utility.hasAsin)

        if len(items) < 1:
            msg = '0 result for query :' + \
                opt['url'] + ', page = ' + str(opt['page'])
            self.sendError(msg)

        # print(opt)
        print(' [C] Num of items:', len(items))

        products = []
        for item in items:
            ad = data.AD()

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
                if err.code != 0:
                    err.setCampaignId(ad['campaignId'])
                    msg = str(err)
                    self.sendError(msg)
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

        if len(brand) < 2:
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

    def getAds(self, query, page=0):
        self.switchProxy()

        opt = {}
        opt['url'] = self.makeQueryUrl(query['query'], page)
        opt['headers'] = self.makeHeaders('mac')
        opt['page'] = page
        opt['query'] = query['query']
        opt['bidPrice'] = query['bidPrice']
        opt['campaignId'] = query['campaignId']
        opt['query_group_id'] = query['query_group_id']

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
        idx = random.randint(0, len(self.proxies)-1)
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
            print(' [C] load proxy %s:%s' % (c[0], c[1]))

    def numQueries(self):
        return len(self.queries)
