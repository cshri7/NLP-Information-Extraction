# this script uses a search engine to parse blograpid7, please install selenium driver
# Daniel Pilgrim-Minaya

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

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random

searchEngines = ['https://google.com/search?q=', 'https://www.bing.com/search?q=', 'https://duckduckgo.com/?q=']

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def parse_data_save(query):

    # chooses between multiple search engines to reduce counterscraping risk
    searchChoice = random.randint(0, 2)
    #chromedriver = os.getcwd()+'/chromedriver'
    #os.environ["webdriver.chrome.driver"] = chromedriver
    #browser = webdriver.Chrome(chromedriver)

    result = []

    url = searchEngines[searchChoice] + query + '+site:https://blog.rapid7.com/'
    #browser.get(url)
    print("URL: {}".format(url))
    try:
        page = urllib2.urlopen(url)
        #soup = BeautifulSoup(browser.page_source,"html5lib")
        soup = BeautifulSoup(page, 'html.parser')
        link = soup.select(".r a") # links

        for l in link:
            # for each link result
            try:
                resulturl = l.get('href')
                d = {}
                html = urllib2.urlopen(resulturl).read()
                d["query"] = query
                d["url"] = resulturl
                d["text"] = text_from_html(html).encode('utf-8').strip()
                result.append(d)
                # print(f'{n_link.text}\n{l.text}')
            except:
                print("Something bad happened")
        df = pd.DataFrame(result)
        df.to_csv("../data/" + query + "blograpid7.csv")
    except Exception as e:
        print("Failure happened for blograpid7 query: {}".format(query))
        print("Exception type: {} \t arguments: {} \t details: {}".format(type(e), e.args, e))
