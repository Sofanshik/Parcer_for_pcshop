import requests
from bs4 import BeautifulSoup
import csv
import os

HEADERS = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
           ' Chrome/80.0.3987.87 Mobile Safari/537.36', 'accept': '*/*'}
HOST = 'https://pcshop.ua'
FILE = 'laptop.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='pagi__link')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='product-thumb')

    laptops = []
    for item in items:
        laptops.append({
            'title': item.find('span', class_='product-thumb__name').get_text(strip=True),
            'price': item.find('span', class_='product-thumb__price').get_text(),
            'information': item.find('div', class_='product-thumb__description').get_text()
        })
    return laptops

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Цена', 'Краткая характеристика'])
        for item in items:
            writer.writerow([item['title'], item['price'], item['information']])

def parse():
    URL = input('Take your URL in site pcshop: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        laptops = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Идет парсинг страницы {page} из {pages_count}')
            html = get_html(URL, params={'page': page})
            laptops.extend(get_content(html.text))
        save_file(laptops, FILE)
        print(f'Получено {len(laptops)} ноутбуков.')
        os.startfile(FILE)
    else:
        print('Error')



parse()