import requests
from bs4 import BeautifulSoup as bs

#эмуляция поведения браузера

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

base_Url = 'https://pushkino.hh.ru/search/vacancy?resume=f45bd12eff079396740039ed1f353133794170&from=resumelist'

def hh_Parse(base_url, headers):
    session = requ