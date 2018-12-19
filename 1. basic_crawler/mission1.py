#
# You need to install the BeautifulSoup4 for Python3 before running this program
# via the following command:
#
# pip3 install beautifulsoup4
#

from bs4 import BeautifulSoup

# 原始 HTML 程式碼
html = """
<html>
<head>
    <title>Hello World</title>
</head>
<body>
    <h2>Test Header<div>3rd</div></h2>
    <p>This is a test.</p>
    <nav>
        <a id="lnk1" href="/path1">Link 1</a>
        <a id="lnk2" href="/path2">Link 2</a>
    </nav>
    <p>Hello, <b class="dark">Bold Text</b></p>
    <p>Hello, <b class="dark hidden">Bold Text</b></p>
    <section attr-post="123">hello</section>
    <section attr-post="456">world</section>
    <div>1st</div>
    <div>2nd</div>
</body>
</html>
"""

# parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# pretty print
print(soup.prettify())

# access the title element and its string content
title = soup.title
print(title)
print(title.string)

# find all the tag 'a'
tags = soup.find_all('a')

for tag in tags:
    print(tag.string, tag.get('href'), tag.get('id'))

# find both a and b
tags = soup.find_all(['a', 'b'])
print(tags)

tags = soup.find_all(['a', 'b'], limit=2)
print(tags)

# find the first element only
tag = soup.find(['a', 'b'])
print(tag)

# By default, soup will search the sub-directories recursively
# find all the DIVs
divs = soup.find_all('div')
print(divs)

# find the DIVs from html.body only
divs = soup.html.body.find_all('div', recursive=False)
print(divs)

# find an element by id
lnk = soup.find(id='lnk1')
print(lnk)

# search all the <a> contains href='/path2'
lnks = soup.find_all('a', href='/path2')
print(lnks)

# element = soup.find_all(attr-post='123')
tags = soup.find_all(attrs={"attr-post": "123"})
print(tags)

# search by CSS class
tags = soup.find_all('b', class_='dark')
print(tags)

# search by CSS selector
tags = soup.select('b.dark.hidden')
print(tags)

# search by string content
lnks = soup.find_all('a', string='Link 1')
print(lnks)

# search with regular expression
import re
lnks = soup.find_all('a', string=re.compile('^Link'))
print(lnks)

# find the parents
lnk = soup.find('a', string='Link 1')
tags = lnk.find_parents('nav')
print(tags)

# find the next siblings
next_lnks = lnk.find_next_siblings('a')
print(next_lnks)

# find the next siblings
prev_lnk = next_lnks[0].find_previous_siblings('a')
print(prev_lnk)
