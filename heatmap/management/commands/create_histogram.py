import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
from django.core.management.base import BaseCommand

from .data_for_histogram import (AVERAGE_AREA_EKB, AVERAGE_AREA_MSK,
                                 AVERAGE_AREA_SPB, AVERAGE_PRICES_EKB,
                                 AVERAGE_PRICES_MSK, AVERAGE_PRICES_SPB,
                                 EKB_DATA, EKB_REGIONS, MSK_DATA, MSK_REGIONS,
                                 SPB_DATA, SPB_REGIONS)


class Command(BaseCommand):
    def add_arguments(self, histogram):
        histogram.add_argument("--city", type=str)
        histogram.add_argument("--data", type=str)

    def handle(self, *args, **options):
        create_histogram(self, options["city"], options["data"])


def create_histogram(self, city, data) -> None:
    """
    creates histogram based on passed data
    by default creates average prices for spb
    """
    CITY = city or "spb"
    NEEDED_DATA = data or "price"

    if CITY == "ekb":
        font = {"size": 10}
        rotation = 0
        area = AVERAGE_AREA_EKB
        price = AVERAGE_PRICES_EKB
        data = EKB_DATA
        regions = EKB_REGIONS
        city_where = "в Екатеринбурге"
    elif CITY == "spb":
        font = {"size": 7}
        area = AVERAGE_AREA_SPB
        price = AVERAGE_PRICES_SPB
        rotation = 90
        data = SPB_DATA
        regions = SPB_REGIONS
        city_where = "в Санкт-Петербурге"
    elif CITY == "msk":
        font = {"size": 9}
        rotation = 0
        area = AVERAGE_AREA_MSK
        price = AVERAGE_PRICES_MSK
        data = MSK_DATA
        regions = MSK_REGIONS
        city_where = "в Москве"

    if NEEDED_DATA == "area":
        stat_data = area
        ru_data_title = "площадь"
    elif NEEDED_DATA == "price":
        stat_data = price
        ru_data_title = "цена"

    offsets = {
        "ekb-area": {"x": 0.05, "y": 1},
        "ekb-price": {"x": 0.15, "y": 1000},
        "spb-area": {"x": 0.05, "y": 1},
        "spb-price": {"x": 0.25, "y": 2000},
        "msk-area": {"x": 0.05, "y": 1},
        "msk-price": {"x": 0.2, "y": 2000},
    }
    matplotlib.rc("font", **font)
    plt.figure(figsize=(len(regions) * 2, 7))
    index = np.arange(len(regions))
    values = stat_data
    plt.title(
        f"Средняя {ru_data_title} квартир {city_where} (всего квартир: {len(data)})",
        fontsize=20,
    )
    plt.bar(index, values, color="b")
    plt.xticks(index, regions)
    plt.xticks(rotation=rotation)
    for x, y in zip(index, values):
        plt.text(
            x - offsets[f"{CITY}-{NEEDED_DATA}"]["x"],
            y + offsets[f"{CITY}-{NEEDED_DATA}"]["y"],
            str(y),
        )
    plt.show()
