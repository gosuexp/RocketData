from bs4 import BeautifulSoup
import requests
import json
from geopandas.tools import geocode


def get_data():
    url = "https://som1.ru/shops/"
    headers = requests.utils.default_headers()
    headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
        }
    )
    q = requests.get(url, headers=headers)
    result = q.content
    soup = BeautifulSoup(result, 'lxml')
    information = soup.find_all(class_='shops-list')

    list_of_links = []
    data_dict = []

    for info in information:
        x = info.find(class_="btn btn-blue")
        link = x.get("href")
        list_of_links.append("https://som1.ru" + link)

    for line in list_of_links:
        q = requests.get(line, headers=headers)
        result = q.content
        soup = BeautifulSoup(result, 'lxml')
        data = soup.find_all("td")
        adress = (data[2].text)[3::]
        name = soup.find("h1").text
        phones = data[5].text.split(' доб. 810, ') + ['8-800-2500-900']
        working_hours = [data[8].text]

        loc = adress
        location = geocode(loc, provider="nominatim", user_agent='my_request')
        point = location.geometry.iloc[0]
        coord = [point.x, point.y]  # координаты
        parametres = {
                 'adress': adress,
                 'latlon': coord,
                 'name': name,
                 'phones': phones,
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