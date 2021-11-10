import functools
import json
import logging
import math
import re
from multiprocessing import Pool
from time import sleep
from typing import Union

import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
from django.core.management.base import BaseCommand

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):

    def add_arguments(self, histogram):
        histogram.add_argument('--city', type=str)

    def handle(self, *args, **options):
        run_scraper(self, options['city'])


city_search = {
    "msk": {"url": "moskva-c3584", "runame": "Москва"},
    "spb": {"url": "sankt_peterburg-c3414", "runame": "Санкт-Петербург"},
    "ekb": {"url": "ekaterinburg-c2653", "runame": "Екатеринбург"},
}


def parse_int(str_: str) -> int:
    """parses integer out of string"""
    newstr = ""
    pattern = re.compile("\\d")
    for i in str_:
        if pattern.match(i):
            newstr += i
    return int(newstr)


def concat_lists(list_of_lists: list) -> list:
    """concats multiple lists into one"""
    new_list = []
    for list_ in list_of_lists:
        if list_:
            new_list.extend(list_)
    return new_list


def get_num_of_pages(city) -> int:
    """returns number of pages of certaing search-request"""
    res = requests.get(f'https://www.domofond.ru/prodazha-kvartiry-{city_search[city]["url"]}')
    soup = BeautifulSoup(res.content, "lxml")
    pages = int(
        soup.find("div", class_="pagination__pagesContainer___up6kR")
        .find_all("li")[-1]
        .text
    )
    return pages


def get_data(city, page: int) -> Union[None, list[dict]]:
    """get flats data for single page"""
    try:
        res = requests.get(
            f'https://www.domofond.ru/prodazha-kvartiry-{city_search[city]["url"]}?Page={page}'
        )
        soup = BeautifulSoup(res.content, "lxml")
        data = soup.find_all("script")[-5].text.lstrip("window.__INITIAL_DATA__ = ")
        data = json.loads(data)["itemsState"]["items"]
        needed_data = [
            {
                "area": math.floor(
                    parse_int(el["price"]) / parse_int(el["pricePerArea"])
                ),
                "pricePerArea": parse_int(el["pricePerArea"]),
                "address": el["address"] + f" {city_search[city]['runame']}",
            }
            for el in data
        ]
        logger.info(f' {page} page is parsed')
        sleep(1)
        return needed_data
    except Exception as e:
        logger.info(f' {e} error occured')
        return None


def get_data_with_mp(city, pages: int) -> list:
    """runs get_data mapping to every page of search"""
    p = Pool(60)
    result = p.map(functools.partial(get_data, city), range(1, pages + 1))
    p.close()
    p.join()
    return concat_lists(result)


def create_json_file(city: str, data: list) -> None:
    """creates json file"""
    with open(f"./site_data/parsed_site_data/{city}_estate_data1.json",
              "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def run_scraper(self, city):
    pages = get_num_of_pages(city)
    result = get_data_with_mp(city, pages)
    create_json_file(city, result)
