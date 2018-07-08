# coding:utf-8
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, date, timedelta

url = 'http://elephant.2chblog.jp/archives/cat_50054740.html'
#11時に取得
yesterday = datetime.strftime(datetime.today() - timedelta(days=1), '%Y%m%d')

class Blog:
    def __init__(self,url):
        self.url= url
        self.requests = requests.get(self.url)
        self.html     = self.requests.text
        self.soup     = BeautifulSoup(self.html,'html.parser')

    def get_title(self):
        titles =  self.soup.find_all('h2')
        return [i.text for i in titles]

    def get_link(self):
        links =  self.soup.find_all('h2')
        return [re.search('"[^"]*',str(i)).group(0).strip('"') for i in links]

    def get_date(self):
        dates =  self.soup.find_all(class_='iTime')
        lists=[]
        for i in dates:
            if int(yesterday) < int(str(i)[18:22]+str(i)[23:25]+str(i)[26:28]):
                lists.append(i)
        return lists

#pageの仕組みはサイトによって違う
def apply_page_num(num,url):
    if num>1:
        url=url+'?p='+str(num)
    return url

def create_data_list(url,pages):
    url_list   = [apply_page_num(num, url) for num in range(1,pages+1)]
    title_list = []
    link_list  = []
    date_list  = []

    for url in url_list:
        instance = Blog(url)
        title_list = title_list + instance.get_title()
        link_list  = link_list  + instance.get_link()
        date_list  = date_list  + instance.get_date()

    #一番最初のレコードを保存する
    past_article_index= len(date_list)
    del title_list[int(past_article_index):]
    del link_list[int(past_article_index):]

    dictionary = {'title':title_list, 'link':link_list}
    df = pd.DataFrame.from_dict(dictionary)
    time.sleep(3)
    return df

blog = Blog(url)
df = create_data_list(url,2)
print (df.head())

def scrape():
    blog = Blog(url)
    df = create_data_list(url,2)
    print (df)
    return df