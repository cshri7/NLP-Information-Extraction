try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time


def parse_page(key, url):
    print url
    driver.maximize_window()
    driver.get(url)
    # time.sleep(5)
    doc = {}
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'html.parser')
    if '/connect/' in url:
        # texts = soup.find('div', class_="content-wrapper").get_text().encode('utf-8').strip()
        heading = soup.find('h1', class_='page-title ng-binding').get_text().encode('utf-8').strip()
        start = soup.find('div', class_='article-body')
        if start:
            article_text = ''
            for item in start.children:
                if item.name == 'p' or item.name == 'h3':
                    article_text += '\n' + ''.join(item.findAll(text = True)).encode('utf-8').strip()
                else:
                    continue
        content = heading+"\r\n"+article_text
    else:
        head1 = soup.find('h1').get_text().encode('utf-8').strip()
        head2 = soup.find('h2').get_text().encode('utf-8').strip()
        # texts = soup.find('div', class_="blog-post__content").get_text().encode('utf-8').strip()
        article = soup.findAll('div', class_="blog-post__content")
        tags = article.findAll(['p', 'h2', 'ul'])
        text = ''
        for tag in tags:
            text += '\n' + ''.join(tag.findAll(text = True)).encode('utf-8').strip()
        content = head1+"\r\n"+head2+"\r\n"+text
    doc["query"] = key
    doc["url"] = url
    doc["text"] = content
    result.append(doc)
    df = pd.DataFrame(result)
    df.to_csv("../data/" + key + "symantec.csv")
    # df.to_csv("data/" + key + "symantec.csv")


driver = webdriver.Chrome()
result = []
df = pd.read_csv("symantec-list.csv")
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
    
driver.quit()
