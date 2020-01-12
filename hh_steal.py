from http.cookiejar import request_host

import requests
from bs4 import BeautifulSoup as bs

#emulaciya povedeniya brauzera
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

base_Url = 'https://pushkino.hh.ru/search/vacancy?resume=f45bd12eff079396740039ed1f353133794170&from=resumelist'

def hh_Parse(base_url, headers):
    session = requests.Session();
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs = {'data-qa': 'vacancy-serp__vacancy'})

        for div in divs:
            name_Vacancy = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'}).text
            link = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'})['href']
            print("{0} {1}".format(name_Vacancy, link))
        #print(divs)
    else:
        print('ERROR')

hh_Parse(base_Url, headers)
