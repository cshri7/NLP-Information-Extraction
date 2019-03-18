try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd


def parse_page(key, url):
    doc = {}
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
    page = urllib2.urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')
    heading = soup.find('h2', class_="page-title").get_text().encode('utf-8').strip()
    start = soup.find('div', class_='content clear-block')
    if start:
        article_text = ''
        for item in start.children:
            if item.name != 'p':
                continue
            else:
                article_text += '\n' + ''.join(item.findAll(text = True)).encode('utf-8').strip()
    content = heading+"\r\n"+article_text
    doc["query"] = key
    doc["url"] = url
    doc["text"] = content
    result.append(doc)
    df = pd.DataFrame(result)
    df.to_csv("../data/" + key + "securityweek.csv")
    # df.to_csv("data/" + key + "securityweek.csv")
    
result = []
df = pd.read_csv("securityweek-list.csv")
rows = df.shape[0]
for i in range(rows):
    keyword = df.key.ix[i]
    link = df.url.ix[i]
    if i==0:
        parse_page(keyword, link)
    else:
        if keyword == df.key.ix[i-1]:
            parse_page(keyword, link)
        else:
            result = []
            parse_page(keyword, link)
