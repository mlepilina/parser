import json
import os.path

import requests
from requests import Response

from bs4 import BeautifulSoup, ResultSet, Tag

from models import Food

SITE_URL = 'https://www.russianfood.com'
FOOD_URI = 'recipes/bytype/'


class PageNotFound(Exception):
    """Страница не найдена"""


class ElementsNotFound(Exception):
    """Страница не найдена"""


class FoodParser:
    """Получает HTML-документ и превращает в модель блюда"""

    def __init__(self, foodid: int):
        self.foodid = foodid
        self.storage = []

    def __make_url(self) -> str:
        return f'{SITE_URL}/{FOOD_URI}?fid={self.foodid}'

    def __get_page(self, url: str) -> str:
        response: Response = requests.get(url=url)
        if response.status_code == 200:
            return response.text

        raise PageNotFound

    def __find_elements(self, page: str) -> ResultSet:
        soup = BeautifulSoup(page, 'html.parser')

        kwargs = {
            'class': 'recipe_l in_seen v2'
        }

        elements: ResultSet = soup.find_all(**kwargs)
        if len(elements):
            return elements

        raise ElementsNotFound

    def run(self):
        url = self.__make_url()
        page = self.__get_page(url)
        elements = self.__find_elements(page=page)

        for element in elements:
            try:
                self.save_element(element)
            except Exception as exc:
                print(f'Была ошибка {exc} при сохранении')

    def save_element(self, element: Tag):
        """Сохраняет модель элемента в общее хранилище класса"""
        food = Food(
            page_ulr=SITE_URL + element.find('a', itemprop='url').attrs['href'],
            title=element.find('span', itemprop='name').text,
            description=element.find('p', itemprop='description').text,
            image_url='https:' + element.find('img').attrs['src']
        )

        self.storage.append(food.__dict__)

    def save_to_json(self, name: str):
        path = os.path.join('storage', f'{name}.json')
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(self.storage, file, ensure_ascii=False, indent=4)

