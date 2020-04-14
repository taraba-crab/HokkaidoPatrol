import requests
from bs4 import BeautifulSoup
from typing import Tuple
from time import sleep

def get_distance_and_time(dep: str, arr: str, delta: float) -> Tuple[float, str]:
    res = requests.get(f"http://d-time.hdb.hkd.mlit.go.jp/info/result.php?dep={dep}&arr={arr}&via=&rsel=c&tsel=")
    sleep(delta)
    soup = BeautifulSoup(res.content, parser="html.parser", features="lxml")

    result = soup\
        .find(id="resulttable")\
        .find("tbody")\
        .find(class_="roh")\
        .find_all("th")

    km = result[0].get_text()
    t = result[2].get_text()

    return float(km[:-2]), t
