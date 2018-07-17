import requests
from bs4 import BeautifulSoup
import re
import time

class Wantedly:
    def __init__(self,url):
        self.url= url
        self.requests = requests.get(self.url)
        self.html     = self.requests.text
        self.soup     = BeautifulSoup(self.html,'html.parser')

    def get_project_urls(self):
        project_urls =  self.soup.find_all('h1',{'class':'project-title'})
        return [('https://www.wantedly.com'+re.search('/projects[^?]*',str(i)).group(0)) for i in project_urls]

def apply_page_num(num,url):
    url = url.replace('page=1','page='+str(num+1))
    return url

def create_data_list(url,pages):
    url_list = [apply_page_num(num, url) for num in range(0,pages)]
    project_url_list  = []
    for url in url_list:
        instance = Wantedly(url)
        project_url_list  = project_url_list  + instance.get_project_urls()
    return project_url_list


def scrape(url):
    wantedly = Wantedly(url)
    return create_data_list(url,5)


    