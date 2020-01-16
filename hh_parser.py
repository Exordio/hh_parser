from http.cookiejar import request_host

import requests
import os
import pandas as pd
from bs4 import BeautifulSoup as bs


excelFile = "vacancyxls.xlsx"

#emulaciya povedeniya brauzera

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

base_Url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=Junior+python+developer&page=0'

def hh_Parse(base_url, headers):
    urls = []; urls.append(base_Url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    
    colum_Names = ['name_Vacancy', 'name_Company', 'vacancy_Payday', 'vacancy_Link', 'vacancy_Responsibility',
                   'vacancy_Requirement']
    vacancy_DF = pd.DataFrame(columns=colum_Names)

    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'lxml') #lxml parsing is faster than vanilla on 30%
        try:
            pages = soup.find_all('a', attrs = {'data-qa': 'pager-page'})
            pages_Count = int(pages[-1].text)
            for i in range(pages_Count):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text=Junior+python+developer&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    else:
        print('ERROR')

    for url in urls:
        #time.sleep(3)
        request = session.get(url, headers = headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs = {'data-qa': 'vacancy-serp__vacancy'})

        for div in divs:
            name_Vacancy = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'}).text
            name_Company = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            link = div.find('a', attrs = {'data-qa': 'vacancy-serp__vacancy-title'})['href']
            try:
                payday = div.find('div', attrs = {'class' : 'vacancy-serp-item__compensation'}).text
            except AttributeError:
                payday = div.find('div', attrs={'class': 'vacancy-serp-item__compensation'})

            vacancy_Responsibility = div.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
            vacancy_Requirement = div.find('div', attrs = {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            vacancy_DF.loc[len(vacancy_DF)] = [name_Vacancy, name_Company, payday, link, vacancy_Responsibility, vacancy_Requirement]

            #print("{} | {} | {} | {}".format(name_Vacancy, payday, name_Company, link))

        #for i in urls:
        #    print(i)
    print(vacancy_DF)
    vacancy_DF.to_excel(excelFile, index=False, encoding="utf-8", sheet_name='Jobs')

    print("ALL PARSED, exec file")
    os.startfile(excelFile)



hh_Parse(base_Url, headers)
