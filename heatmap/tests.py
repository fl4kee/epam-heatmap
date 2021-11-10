# API key in test is not valid
import json
from unittest import mock

import requests_mock
from django.test import TestCase

from heatmap.management.commands.get_locations import (  # type: ignore
    get_locations, open_file)
from heatmap.management.commands.scraper import get_data  # type: ignore


class ScraperTestCase(TestCase):
    def setUp(self):
        with open("heatmap/test_data/scraper_test_page.html", "r", encoding="utf-8") as f:
            self.FILE = ''.join(f.readlines())

    def test_get_data(self):
        with requests_mock.Mocker() as m:
            m.get(
                "https://www.domofond.ru/prodazha-kvartiry-moskva-c3584?Page=1", text=self.FILE
            )
            with open("heatmap/test_data/scraper-test-result.json", encoding="utf-8") as f:
                test_file = json.load(f)
            self.assertEqual(get_data('msk', 1), test_file)


class GetLocationsTestCase(TestCase):
    def setUp(self):
        with open("heatmap/test_data/get-locations-input-data.json", encoding="utf-8") as f:
            self.INPUT_FILE = ''.join(f.readlines())

        with open("heatmap/test_data/get-locations-geocoder-test-resp.json", encoding="utf-8") as f:
            self.GEOCODER_RESP = ''.join(f.readlines())

    @mock.patch('heatmap.management.commands.get_locations.open_file', autospec=True)
    def test_get_locations(self, mock_open_file):
        mock_open_file.return_value = json.loads(self.INPUT_FILE)
        with requests_mock.Mocker() as m:
            m.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address=%D0"
                "%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0,%20%D0%9F%D0%BE%D0%BB%D0%BE"
                "%D1%86%D0%BA%D0%B0%D1%8F%20%D1%83%D0%BB%D0%B8%D1%86%D0%B0,%20"
                "16%20%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&key="
                "<YOUR API KEY>",
                text=self.GEOCODER_RESP,
            )
            self.assertEqual(get_locations('msk', 0), {
                'lat': 55.7337228,
                'lng': 37.42492790000001,
                'area': 59,
                'pricePerArea': 261667,
                'region': 'Zapadnyy administrativnyy okrug',
                'formatted_address': 'Polotskaya Ulitsa, 16, Moskva, Russia, 121351',
                'place_id': 'Ei1Qb2xvdHNrYXlhIFVsaXRzYSwgMTYsIE1vc2t2YSwgUnVzc2lhLCA'
                            'xMjEzNTEiGhIYChQKEgntvWePwk61RhEdyyfNkocEJBAQ'
            })
