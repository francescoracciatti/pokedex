"""
This module provides unittest for public endpoints.
"""

import argparse
import sys
import unittest
from abc import ABC
from ipaddress import ip_address
from typing import Dict, Any, List, Union

import requests as requests


class JSON(ABC):
    """
    Provides utility functions for json.
    """

    @classmethod
    def deepsort(cls, obj: Union[Dict[str, Any], List[Any]]) -> List[Any]:
        """
        Recursively sort the given json.
        In particular it sorts any list it finds in the json, and converts dicts to lists of (key, value) pairs in order
        to make them orderable.

        :param obj: the json
        :return: the sorted json in format of a list of (key, value) pairs
        """
        if isinstance(obj, dict):
            return sorted((k, cls.deepsort(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(cls.deepsort(x) for x in obj)
        else:
            return obj


class UnrecognizedConfiguration(RuntimeError):
    """
    Raised in case of unrecognized configuration.
    """
    pass


class UnrecognizedPokemon(RuntimeError):
    """
    Raised in case of unrecognized pokemon.
    """
    pass


class ExpectedJSON(ABC):
    """
    Provides the json containing expected data.
    """

    # Tailors the expected json basing on the language and the version
    LANGUAGE = 'en'
    VERSION = 'red'

    @staticmethod
    def basic_info(name: str, language: str = LANGUAGE, version: str = VERSION) -> Dict[Any, Any]:
        """
        Gets the json describing the given pokemon.

        :param name: the name of the pokemon
        :param language: the language of the description, supports 'en' only
        :param version: the pokemon version, supports 'red' only
        :return: the json containing the description
        """
        # Supports en + red, only
        if language != 'en' and version != 'red':
            raise UnrecognizedConfiguration(f"Configuration not supported, language {language}, version {version}")

        if name == 'mewtwo':
            return {
                "name": "mewtwo",
                "description": "It was created by a scientist after years of horrific gene splicing "
                               "and DNA engineering experiments.",
                "habitat": "rare",
                "isLegendary": True
            }

        if name == 'zubat':
            return {
                "name": "zubat",
                "description": "Forms colonies in perpetually dark places. "
                               "Uses ultrasonic waves to identify and approach targets.",
                "habitat": "cave",
                "isLegendary": False
            }

        if name == 'ditto':
            return {
                "name": "ditto",
                "description": "Capable of copying an enemy's genetic code to instantly transform itself into "
                               "a duplicate of the enemy.",
                "habitat": "urban",
                "isLegendary": False
            }

        raise UnrecognizedPokemon(f"Pokemon {name} unrecognized")

    @staticmethod
    def translated(name: str, language: str = LANGUAGE, version: str = VERSION) -> Dict[Any, Any]:
        """
        Gets the json containing the translated description of the given pokemon.

        :param name: the name of the pokemon
        :param language: the language of the description, supports 'en' only
        :param version: the pokemon version, supports 'red' only
        :return: the json containing the description
        """
        # Supports en + red, only
        if language != 'en' and version != 'red':
            raise UnrecognizedConfiguration(f"Configuration not supported, language {language}, version {version}")

        if name == 'mewtwo':  # Legendary, uses Yoda
            return {
                "name": "mewtwo",
                "description": "Created by a scientist after years of horrific gene splicing "
                               "and dna engineering experiments,  it was.",
                "habitat": "rare",
                "isLegendary": True
            }

        if name == 'zubat':  # Cave, uses Yoda
            return {
                "name": "zubat",
                "description": "Forms colonies in perpetually dark places."
                               "Ultrasonic waves to identify and approach targets,  uses.",
                "habitat": "cave",
                "isLegendary": False
            }

        if name == 'ditto':  # Neither legendary nor cave, use shakespeare
            return {
                "name": "ditto",
                "description": "Capable of copying an foe's genetic code "
                               "to instantly transform itself into a duplicate of the foe.",
                "habitat": "urban",
                "isLegendary": False
            }

        raise UnrecognizedPokemon(f"Pokemon {name} unrecognized")


class TestAPI(unittest.TestCase):

    # Endpoints
    ENDPOINT_BASIC_INFO = None
    ENDPOINT_TRANSLATED = None

    @staticmethod
    def init(host: str, port: int) -> None:
        """
        Initializes the Test class.

        :param host: the host ip address
        :param port: the port
        """
        TestAPI.ENDPOINT_BASIC_INFO = f"http://{host}:{port}/pokemon"
        TestAPI.ENDPOINT_TRANSLATED = f"http://{host}:{port}/pokemon/translated"

    def setUP(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_basic_info_unknown_pokemon(self) -> None:
        """
        Test the response when asking for a unknown pokemon.
        """
        response = requests.get(f"{self.ENDPOINT_BASIC_INFO}/nomekop")
        self.assertEqual(404, response.status_code,
                         f"Expected 404 for unknown pokemon, status code {response.status_code}")

    def test_translated_unknown_pokemon(self) -> None:
        """
        Test the response when asking for a unknown pokemon.
        """
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/nomekop")
        self.assertEqual(404, response.status_code,
                         f"Expected 404 for unknown pokemon, status code {response.status_code}")

    def test_basic_info(self) -> None:
        """
        Tests the basic info for the pokemon mewtwo.
        """
        # Gets basic info of mewtwo
        response = requests.get(f"{self.ENDPOINT_BASIC_INFO}/mewtwo")
        self.assertEqual(200, response.status_code,
                         f"Cannot satisfy the GET request, status code {response.status_code}")
        json_actual = response.json()
        self.assertEqual(JSON.deepsort(ExpectedJSON.basic_info('mewtwo')), JSON.deepsort(json_actual), "JSON mismatch")

    def test_translated_info_legendary(self) -> None:
        """
        Tests the translated info for the pokemon mewtwo (legendary pokemon).
        """
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/mewtwo")
        self.assertIn(response.status_code, [200, 429],
                      f"Cannot satisfy the GET request, status code {response.status_code}")
        json_actual = response.json()

        if response.status_code == 200:
            json_expected = ExpectedJSON.translated('mewtwo')
        else:  # 429 Too many requests
            json_expected = ExpectedJSON.basic_info('mewtwo')

        self.assertEqual(JSON.deepsort(json_expected), JSON.deepsort(json_actual), "JSON mismatch")

    def test_translated_info_cave(self) -> None:
        """
        Tests the translated info for the pokemon zubat (cave pokemon).
        """
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/zubat")
        self.assertIn(response.status_code, [200, 429],
                      f"Cannot satisfy the GET request, status code {response.status_code}")
        json_actual = response.json()

        if response.status_code == 200:
            json_expected = ExpectedJSON.translated('zubat')
        else:  # 429 Too many requests
            json_expected = ExpectedJSON.basic_info('zubat')

        self.assertEqual(JSON.deepsort(json_expected), JSON.deepsort(json_actual), "JSON mismatch")

    def test_translated_info_normal(self) -> None:
        """
        Tests the translated info for normal pokemon (neither legendary nor cave).
        """
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/ditto")
        self.assertIn(response.status_code, [200, 429],
                      f"Cannot satisfy the GET request, status code {response.status_code}")
        json_actual = response.json()

        if response.status_code == 200:
            json_expected = ExpectedJSON.translated('ditto')
        else:  # 429 Too many requests
            json_expected = ExpectedJSON.basic_info('ditto')

        self.assertEqual(JSON.deepsort(json_expected), JSON.deepsort(json_actual), "JSON mismatch")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', dest='host', required=True, help='target host', type=ip_address)
    parser.add_argument('--port', dest='port', required=True, help='target port', type=int)
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    print(f"Running tests, looking for pokedex at {args.host}:{args.port}")

    sys.argv[1:] = args.unittest_args
    TestAPI.init(args.host, args.port)
    unittest.main()
