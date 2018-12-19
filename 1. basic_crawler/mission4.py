#
# Before running this script you need to do:
# pip3 install aiohttp
# pip3 install aiodns
#

import aiohttp
import asyncio
from bs4 import BeautifulSoup


def parse(htmldoc):
    soup = BeautifulSoup(htmldoc, 'html.parser')

    def has_asin(tag):
        return tag.has_attr('data-asin')
    tags = soup.find_all(has_asin)

    results = []
    for tag in tags:
        product_id = tag.get('data-asin')
        imgsrc = tag.find('img').get('src')

        whole = tag.find(class_='sx-price-whole')
        fraction = tag.find(class_='sx-price-fractional')

        if whole is None or fraction is None:
            continue

        price = float(whole.string + '.' + fraction.string)
        results.append({
            'product_id': product_id,
            'imgsrc': imgsrc,
            'price': price
        })

    return results


async def fetch(session, url):
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def crawler(keyword):
    print('Start crawling', keyword)
    url = "https://www.amazon.com/s/ref=nb_sb_noss?field-keywords=" + keyword
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        products = parse(html)
        print(products)

tasks = []
tasks.append(crawler('prenatal DHA supplement'))
tasks.append(crawler('Wall Mount Shelf'))
tasks.append(crawler('iphone%20case'))
tasks.append(crawler('building%20toys'))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))

# def crawler(keyword):
#     url = "https://www.amazon.com/s/ref=nb_sb_noss?field-keywords=" + keyword

#     USER_AGENT_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
#     USER_AGENT_IPHONE = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"

#     headers = {
#         'User-Agent': USER_AGENT_MAC
#     }

#     req = requests.get(url, headers=headers)

#     if req.status_code == requests.codes.ok:
#         results = parse(req.text)
#         print(results)
#         print('Number of products:', len(results))


# keyword = 'prenatal DHA supplement'
# # keyword = 'Wall Mount Shelf'
# # keyword = 'iphone%20case'
# # keyword = 'building%20toys'
# crawler(keyword)
