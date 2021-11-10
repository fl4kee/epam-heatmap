import json
import math

SPB_REGIONS = {
    "Адмиралтейский": "Admiralteyskiy",
    "Васильевский о-в": "Vasileostrovskiy",
    "Выборгский": "Vyborgskiy",
    "Калининский": "Kalininskiy",
    "Кировский": "Kirovskiy",
    "Колпинский": "Kolpinskiy",
    "Красногв-ский": "Krasnogvardeyskiy",
    "Красносельский": "Krasnosel'skiy",
    "Московский": "Moskovskiy",
    "Курортный": "Kurortnyy",
    "Кронштадтский": "Kronshtadtskiy",
    "Невский": "Nevskiy",
    "Петроградский": "Petrogradskiy",
    "Петродворцовый": "Petrodvortsovyy",
    "Приморский": "Primorskiy",
    "Пушкинский": "Pushkinskiy",
    "Фрунзенский": "Frunzenskiy",
    "Цетральный": "Tsentral'nyy",
}

MSK_REGIONS = {
    "Югозападный": "Yugo-Zapadnyy administrativnyy okrug",
    "Северо-Восточный": "Severo-Vostochnyy administrativnyy okrug",
    "Юго-Восточный": "Yugo-Vostochnyy administrativnyy okrug",
    "Восточный": "Vostochnyy administrativnyy okrug",
    "Центральный": "Tsentralnyy administrativnyy okrug",
    "Северный": "Severnyy administrativnyy okrug",
    "Южный": "Yuzhnyy administrativnyy okrug",
    "Западный": "Zapadnyy administrativnyy okrug",
    "Северо-Западный": "Severo-Zapadnyy administrativnyy okrug",
    "Зеленоградский": "Zelenogradskiy administrativnyy okrug",
    "Новомосковский": "Novomoskovsky Administrative Okrug",
}

EKB_REGIONS = {
    "Железнодорожный": "Zheleznodorozhnyy",
    "Верх-Исетский": "Verkh-Isetskiy",
    "Чкаловский": "Chkalovskiy",
    "Ленинский": "Leninskiy",
    "Октябрьский": "Oktyabr'skiy",
    "Кировский": "Kirovskiy",
    "Орджоникидзевский": "Ordzhonikidzevskiy",
}


def get_data(city: str) -> tuple[list, list, dict]:
    """calculates average prices and areas of every region of the city"""
    if city == "spb":
        with open("./heatmap/data/spb_locations.json", encoding="utf-8") as f:
            DATA = json.load(f)
        regions = SPB_REGIONS

    elif city == "msk":
        with open("./heatmap/data/msk_locations.json", encoding="utf-8") as f:
            DATA = json.load(f)
        regions = MSK_REGIONS

    elif city == "ekb":
        with open("./heatmap//data/ekb_locations.json", encoding="utf-8") as f:
            DATA = json.load(f)
        regions = EKB_REGIONS

    average_prices = []
    average_areas = []

    for region in regions.values():
        total_price = 0
        total_area = 0
        count = 0
        for el in DATA:
            if el["region"] == region:
                total_price += el["pricePerArea"]
                total_area += el["area"]

                count += 1
        average_prices.append(math.floor(total_price / count))
        average_areas.append(math.floor(total_area / count))

    return (average_prices, average_areas, DATA)


AVERAGE_PRICES_SPB, AVERAGE_AREA_SPB, SPB_DATA = get_data("spb")
AVERAGE_PRICES_MSK, AVERAGE_AREA_MSK, MSK_DATA = get_data("msk")
AVERAGE_PRICES_EKB, AVERAGE_AREA_EKB, EKB_DATA = get_data("ekb")
