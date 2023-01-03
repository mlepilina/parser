import requests
from requests import Response

from bs4 import BeautifulSoup, ResultSet

SITE_URL = 'https://www.russianfood.com'
FOOD_URI = 'recipes/bytype/'
SALAD_ID = 527


response: Response = requests.get(url=f'{SITE_URL}/{FOOD_URI}', params={'fid': SALAD_ID})
try:
    1/ 0
except Exception as exc:
    pass
print(response)

soup = BeautifulSoup(response.text, 'html.parser')

kwargs = {
    'class': 'recipe_l in_seen v2'
}

elements: ResultSet = soup.find_all(**kwargs)

print(soup)


