try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re
from bs4 import BeautifulSoup
import json
import datetime
from dateutil.parser import parse
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    # soup = BeautifulSoup(body, 'html.parser')
    texts = body.findAll(text=True)
    print(texts)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def parse_data_save(query):
    # query = "APT1"
    url = 'https://www.fireeye.com/search.html?q=%s&numResultsPerPage=50' % query

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    all_links = soup.find_all('a', class_="a03_link")
    print("Num links: {}".format(len(all_links)))
    result = []
    for link in all_links:
        d = {}
        url = "https://www.fireeye.com/" + link.get("href")
        html = urllib2.urlopen(url)
        s = BeautifulSoup(html, 'html.parser')
        main = s.find('main')
        if not main:
            continue
        doc = main.find('div', class_="entrytext section")
        if not doc:
            doc = main.find('div', class_="g-content")
        d["url"] = url 
        d["query"] = query
        d["text"] = text_from_html(doc).encode('utf-8').strip() if doc else ""
        result.append(d)

    df = pd.DataFrame(result)
    df.to_csv("../data/" + query + "fireeye.csv")
    return df
