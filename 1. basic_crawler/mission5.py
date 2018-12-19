import aiohttp
import asyncio
from bs4 import BeautifulSoup


class ProxyCrawler():
    def __init__(self):
        self.proxyhost = '199.101.97.183'  # default proxy server
        self.proxyport = '60099'  # default proxy port
        self.account = 'bittiger'
        self.passwd = 'cs504'
        self.url = ''
        pass

    def setUrl(self, url):
        self.url = url

    def setProxy(self, host, port):
        self.proxyhost = host
        self.proxyport = str(port)

    def parse(self, html):
        print(html)

    async def fetch(self, session, url):
        proxy = 'http://'+self.account+':' + self.passwd + \
            '@' + self.proxyhost+':'+self.proxyport
        # proxy = 'http://bittiger:cs504@199.101.97.183:60099'
        async with session.get(url, proxy=proxy) as res:
            return await res.text()

    async def run(self):
        USER_AGENT_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
        USER_AGENT_IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
        headers = {'User-Agent': USER_AGENT_MAC}

        print('Start crawling', self.url)
        async with aiohttp.ClientSession(headers=headers) as session:
            html = await self.fetch(session, self.url)
            self.parse(html)


class MyIPCrawler(ProxyCrawler):
    def __init__(self):
        return super().__init__()

    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tag = soup.find(
            'table', class_='table table-bordered table-striped')
        tags = tag.find_all('td')
        result = tags[1].find('strong').get_text()
        print(result)


if __name__ == '__main__':
    crawler = MyIPCrawler()
    crawler.setUrl('http://www.toolsvoid.com/what-is-my-ip-address')
    crawler.setProxy('199.101.97.183', 60099)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*[crawler.run()]))
