import requests
from requests import Response

from bs4 import BeautifulSoup, ResultSet, Tag

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

    def __make_url(self) -> str:
        return f'{SITE_URL}/{FOOD_URI}?fid={self.foodid}'

    def __get_page(self, url: str) -> str:
        response: Response = requests.get(url = url)
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
            self.save_element(element)

    def save_element(self, element: Tag):
        """Сохраняет модель элемента в общее хранилище класса"""
        #TODO Реализовать

salad_parser = FoodParser(foodid=527)
salad_parser.run()
