import functools
import json
import logging
import math
import statistics
from multiprocessing import Pool
from time import sleep
from typing import Union

import requests  # type: ignore
from django.core.management.base import BaseCommand

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Command(BaseCommand):
    def add_arguments(self, histogram):
        histogram.add_argument("--city", type=str)

    def handle(self, *args, **options):
        run_get_locations(self, options["city"])


def open_file(city):
    with open(
        f"./site_data/parsed_site_data/{city}_estate_data1.json", encoding="utf-8"
    ) as f:
        return json.load(f)


def get_region(data: dict, city: str) -> Union[None, str]:
    """depending on current city returns condition for getting its region"""
    for region in data["address_components"]:
        condition = False
        if city == "spb" or city == "ekb":
            condition = region["types"] == ["administrative_area_level_3", "political"]
        elif city == "msk":
            condition = region["types"] == [
                "political",
                "sublocality",
                "sublocality_level_1",
            ]
        if condition:
            return region["long_name"]
    return None


def get_locations(city, index: int) -> Union[None, dict]:
    """get detailed information for one address with help of Geocoder"""
    data = open_file(city)
    address = "%20".join(data[index]["address"].split())
    real_address_url = (f'https://maps.googleapis.com/maps/api/geocode/json?address={address}'
                        '&key=<YOUR API KEY>')

    try:
        res = requests.get(real_address_url).json()
        if city == "spb":
            region = get_region(res["results"][0], "spb")
        elif city == "ekb":
            region = get_region(res["results"][0], "ekb")
        elif city == "msk":
            region = get_region(res["results"][0], "msk")

        formatted_address = res["results"][0]["formatted_address"]
        location = res["results"][0]["geometry"]["location"]
        place_id = res["results"][0]["place_id"]
        res_obj = {
            "lat": location["lat"],
            "lng": location["lng"],
            "area": data[index]["area"],
            "pricePerArea": data[index]["pricePerArea"],
            "region": region,
            "formatted_address": formatted_address,
            "place_id": place_id,
        }
        logger.info(f' {index  + 1} address is processed')
        sleep(1)
        return res_obj
    except Exception as e:
        logger.info(f' {e} error occured')
        return None


def get_locations_mp(city, elements: int) -> list:
    """running get_locations with multiprocessing"""
    p = Pool(30)
    result = p.map(functools.partial(get_locations, city), range(elements))
    p.close()
    p.join()
    return result


def get_average_price_and_area(flats: list) -> dict:
    """returns data with average price and area of passed list of addresses"""
    average_price = statistics.mean([flat["pricePerArea"] for flat in flats])
    average_area = statistics.mean([flat["area"] for flat in flats])
    return {
        "pricePerArea": math.floor(average_price),
        "area": math.floor(average_area),
        "lng": flats[0]["lng"],
        "lat": flats[0]["lat"],
        "region": flats[0]["region"],
        "address": flats[0]["formatted_address"],
    }


def create_set_of_locations(data: list[dict]) -> list[dict]:
    """
    removes duplicating addresses
    returns set of addresses with average area and price for each address
    """
    set_of_addresses = []
    list_of_adressess = []
    new_dict = {}
    for i in data:
        if i:
            if i["formatted_address"] not in list_of_adressess:
                new_dict[i["formatted_address"]] = [i]
                list_of_adressess.append(i["formatted_address"])
            else:
                new_dict[i["formatted_address"]].append(i)
    for value in new_dict.values():
        set_of_addresses.append(get_average_price_and_area(value))
    return set_of_addresses


def create_json_file(city: str, data: list[dict]) -> None:
    """creates json file in locations folder"""
    with open(
        f"./site_data/locations/{city}_locations.json", "w", encoding="utf-8"
    ) as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def run_get_locations(self, city):
    locations = get_locations_mp(city, 10)
    set_of_locations = create_set_of_locations(locations)
    create_json_file(city, set_of_locations)
