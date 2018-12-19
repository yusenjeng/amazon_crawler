from bs4 import BeautifulSoup

with open('mission2.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

    # remove double spaces in the class_
    lnks = soup.find_all(
        'a', class_='a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal')
    print('Number of products:', len(lnks))

    for lnk in lnks:
        title = lnk.get('title')
        href = lnk.get('href')
        # print('=>', title)
        # print('  ', href)

    # list tags that contains the attribute 'data-asin'
    # 'data-asin' 是產品 ID
    def has_asin(tag):
        return tag.has_attr('data-asin')
    tags = soup.find_all(has_asin)
    print('Number of products:', len(tags))
    for tag in tags:
        print('\t', tag.get('data-asin'))
        print('\t', tag.find('img').get('src'))

        whole = tag.find(class_='sx-price-whole')
        fraction = tag.find(class_='sx-price-fractional')

        if whole is None or fraction is None:
            continue
        price = float(whole.string + '.' + fraction.string)
        print('\t', price)

        # price_tags = tag.find_all(class_='a-offscreen')
        # price = ''
        # if len(price_tags) == 1:
        #     price = price_tags[0].string
        # elif len(price_tags) == 2:
        #     price = price_tags[1].string

        # if price == '[Sponsored]':
        #     price = 0
        # elif price == '':
        #     price = 0
        # elif ' - ' in price:    # happend with keyword: iphone%20case
        #     price = float(price.split(' - ')[0][1:])
        # else:
        #     price = float(price[1:])
        # print('\t', price)

    # selector = '#result_21 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div.a-row.a-spacing-none.scx-truncate-medium.sx-line-clamp-2 > a'
    # tags = soup.select(selector)
    # print('Number of products:', len(tags))
    # for tag in tags:
    #     print('\t', tag.get('title'))
    #     print('\t', tag.get('href'))
