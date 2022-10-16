import re

from bs4 import BeautifulSoup
import requests
import json


def get_data():
    url = "https://naturasiberica.ru/our-shops"
    q = requests.get(url)
    result = q.content
    soup = BeautifulSoup(result, 'lxml')
    information = soup.find_all(class_="card-list__link")

    list_of_links = []
    data_dict = []

    for info in information:
        link = info.get("href")
        list_of_links.append("https://naturasiberica.ru" + link)

    for line in list_of_links:
        q = requests.get(line)
        result = q.content
        soup = BeautifulSoup(result, 'lxml')
        data = soup.find(class_="card-list__link").text
        adress = re.sub("^\s+|\n|\t|\r|\s+$", '', data)
        name = "Natura Siberica"
        working_hours = [
            ' '.join(soup.find(class_="original-shops__settings-block").
                     find(class_="original-shops__info").
                     find(class_="shop-schedule original-shops__schedule").text.split('\r\n'))[:-2]
        ]
        parametres = {
            'adress': adress,
            'name': name,
            # 'phones': phones,
            'working_hours': working_hours
        }
        data_dict.append(parametres)

        with open('data.json', 'w') as json_file:
            json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
            print('!')


def main():
    get_data()


if __name__ == '__main__':
    main()
