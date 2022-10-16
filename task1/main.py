from bs4 import BeautifulSoup
import requests
import json
from geopandas.tools import geocode


def get_data():
    url = "https://oriencoop.cl/sucursales.htm"
    q = requests.get(url)
    result = q.content
    soup = BeautifulSoup(result, 'lxml')
    information = soup.find_all(class_='sub-menu')

    list_of_links = []
    data_dict = []

    for info in information:
        city = info.find("li")
        x = city.find('a')
        link = x.get("href")
        list_of_links.append('https://oriencoop.cl' + link)

    for line in list_of_links:
        q = requests.get(line)
        result = q.content
        soup = BeautifulSoup(result, 'lxml')
        data = soup.find(class_="s-dato").find_all("p")
        adress = data[0].text[11::].strip()
        name = "Oriencoop"
        phones = [data[1].text[10::].strip(), "600 200 0015", "+56712207838"]
        agent = data[2].text[8::].strip()
        working_hours = data[3].text[10::].split("\n")[1:3]

        loc = data[0].text[11::].strip().replace('local', '')
        location = geocode(loc, provider="nominatim", user_agent='my_request')
        point = location.geometry.iloc[0]
        coord = [point.x, point.y]  # координаты

        parametres = {
                'adress': adress,
                'latlon': coord,
                'name': name,
                'phones': phones,
                'agent': agent,
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