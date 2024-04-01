import os
from unicodedata import normalize
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint
from logger2 import logger

HOST = 'https://spb.hh.ru/search/vacancy?text=python+django+Flask&salary=&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list'


def get_headers():
    return Headers(browser='firefox', os='win').generate()


SOURCE = requests.get(HOST, headers=get_headers()).text
bs = BeautifulSoup(SOURCE, features='lxml')

articles = bs.find_all(class_='vacancy-serp-item-body')


def get_articless():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def get_articles():
            vacancy_list = []
            for article in articles:
                link = article.find('a')['href']
                salary = article.find('span', class_='bloko-header-section-2')
                #  a = normalize('NFKD', name)
                try:
                    salary = normalize('NFKD', salary.text)
                except:
                    continue
                company = normalize('NFKD', article.find('a', class_='bloko-link bloko-link_kind-tertiary').text)
                city = normalize('NFKD', article.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text)
                vacancy_list.append({
                    'Ссылка': link,
                    'Зарплата': salary,
                    'Компания': company,
                    'Город': city,
                })
            return vacancy_list

        get_articles()

if __name__ == '__main__':
    get_articless()