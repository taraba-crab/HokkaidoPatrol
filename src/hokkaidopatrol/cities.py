from bs4 import BeautifulSoup
import re

html = open(f"{__file__}/../html/citymap.html", encoding="utf-8").read()
soup = BeautifulSoup(html, "html.parser")
a = soup.find_all(value=re.compile("[0-9]{5}"))

def _mapping(tags_with_value):
    for tag in tags_with_value:
        yield tag["value"], tag.get_text()

cities = dict(_mapping(a))
cities_to_num = {v: k for k, v in cities.items()}
