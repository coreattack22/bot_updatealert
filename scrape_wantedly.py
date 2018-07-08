import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time

url = 'https://www.wantedly.com/projects?type=mixed&page=1&occupation_types%5B%5D=engineer&hiring_types%5B%5D=mid_career&locations%5B%5D=tokyo&keywords%5B%5D=python'

class Wantedly:
    def __init__(self,url):
        self.url= url
        self.requests = requests.get(self.url)
        self.html     = self.requests.text
        self.soup     = BeautifulSoup(self.html,'html.parser')

    def get_companies(self):
        list=[]
        companies =  self.soup.find_all('a',{'class':'wt-company'})
        for i in companies:
            if str(i).find('img') == -1:
                list.append(i.string)
        return list

    def get_project_names(self):
        project_names =  self.soup.find_all('h1',{'class':'project-title'})
        return [(i.text.replace('\\n','')) for i in project_names]

    def get_project_urls(self):
        project_urls =  self.soup.find_all('h1',{'class':'project-title'})
        return [('https://www.wantedly.com'+re.search('/projects[^?]*',str(i)).group(0)) for i in project_urls]

def apply_page_num(num,url):
    url = url.replace('page=1','page='+str(num+1))
    return url

def create_data_list(url,pages):
    url_list = [apply_page_num(num, url) for num in range(0,pages)]
    company_list      = []
    project_name_list = []
    project_url_list  = []

    for url in url_list:
        instance = Wantedly(url)
        company_list      = company_list      + instance.get_companies()
        project_name_list = project_name_list + instance.get_project_names()
        project_url_list  = project_url_list  + instance.get_project_urls()

    dictionary = {'タイトル:':company_list, 'URL:':project_name_list, 'project_url':project_url_list}
    df = pd.DataFrame.from_dict(dictionary)
    time.sleep(3)
    return df

wantedly = Wantedly(url)
df = create_data_list(url,2)
print (df)
df.head()
