import json
from urllib.parse import urljoin

import requests

from bs4 import BeautifulSoup


KEYWORDS = ["django","flask"]
HEADERS = {'user-agent': 'app/0.0.1'}


def get_item_text(html, attrs, default = None):
    element = html.find(attrs=attrs)
    if element:
        return element.get_text()
    return default

def main():
    vacancies = []
    links = []
    url = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
    for _ in range(2):
        r = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        for l in soup.find_all(attrs={"class":"serp-item__title"}):
            url = l.get('href')
            if url.startswith('http'):
                links.append(url)
        url = urljoin(url, soup.find(attrs={"data-qa":"pager-next"}).get('href'))


    for link in links:
        r = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        description =  get_item_text(soup, {'class': 'g-user-content'}, default='').lower()
        if not any([kw for kw in KEYWORDS if kw in description]):
            continue
        company = get_item_text(soup, {'class': 'vacancy-company-name'})
        salary = get_item_text(soup, {'class': 'vacancy-salary'})
        city = get_item_text(soup, {'data-qa': 'vacancy-view-location'})
        vacancies.append({'url': link,  'salary': salary, 'company': company, 'city':city})


    with open('vacancies.json', 'w') as fp:
        json.dump(vacancies, fp, indent=4)


if __name__ == '__main__':
    main()
