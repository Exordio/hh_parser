from http.cookiejar import request_host

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs


#emulaciya povedeniya brauzera
headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

base_Url = 'https://hh.ru/search/vacancy?area=1&st=searchVacancy&text=Junior+python+developer&from=suggest_post'

def hh_Parse(base_url, headers):
    session = requests.Session();
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs = {'data-qa': 'vacancy-serp__vacancy'})

        colum_Names = ['name_Vacancy', 'name_Company', 'vacancy_Link', 'vacancy_Payday']

        vacancy_DF = pd.DataFrame(columns = colum_Names)

        for div in divs:
            name_Vacancy = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'}).text
            name_Company = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            link = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'})['href']
            try:
                payday = div.find('div', attrs = {'class' : 'vacancy-serp-item__compensation'}).text
            except AttributeError:
                payday = div.find('div', attrs={'class': 'vacancy-serp-item__compensation'})

            vacancy_DF.loc[len(vacancy_DF)] = [name_Vacancy, name_Company, link, payday]
            #print("{} | {} | {} | {}".format(name_Vacancy, payday, name_Company, link))

        print(vacancy_DF)
    else:
        print('ERROR')

hh_Parse(base_Url, headers)
