"""
This module provides unittest for public endpoints.
"""

import sys
import unittest
from abc import ABC
from typing import Dict, Any

import requests as requests

from src.utils.utils import JSON


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
                               "and DNA engineering experiments, it was.",
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

    # Default configuration
    HOST = '127.0.0.1'
    PORT = 5000

    # Endpoints
    ENDPOINT_BASIC_INFO = f"http://{HOST}:{PORT}/pokemon"
    ENDPOINT_TRANSLATED = f"http://{HOST}:{PORT}/pokemon/translated"

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
        response = requests.get(f"{self.ENDPOINT_BASIC_INFO}/nomekop")
        self.assertEqual(404, response.status_code,
                         f"Expected 404 for unknown pokemon, status code {response.status_code}")

    def test_basic_info(self) -> None:
        """
        Tests the basic info provided by pokedex for the pokemon mewtwo.
        """
        # Gets basic info of mewtwo
        response = requests.get(f"{self.ENDPOINT_BASIC_INFO}/mewtwo")
        self.assertEqual(200, response.status_code,
                         f"Cannot satisfy the GET request, status code {response.status_code}")
        json_actual = response.json()
        self.assertEqual(JSON.deepsort(ExpectedJSON.basic_info('mewtwo')), JSON.deepsort(json_actual), "JSON mismatch")

    def test_translated_info_legendary(self) -> None:
        """
        Tests the basic info provided by pokedex for the pokemon mewtwo (legendary pokemon).
        """
        # Gets basic info of mewtwo
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/mewtwo")
        if response.ok:
            json_actual = response.json()
        else:
            self.fail(f"Cannot satisfy the GET request, status code {response.status_code}")

        if response.status_code == 200:
            json_expected = ExpectedJSON.translated('mewtwo')
        elif response.status_code == 502:  # Bad Gateway, uses standard description
            json_expected = ExpectedJSON.basic_info('mewtwo')
        else:
            self.fail(f"Status code {response.status_code} not handled")

        self.assertEqual(JSON.deepsort(json_expected), JSON.deepsort(json_actual), "JSON mismatch")

    def test_translated_info_cave(self) -> None:
        """
        Tests the basic info provided by pokedex for the pokemon zubat (cave pokemon).
        """
        # Gets basic info of mewtwo
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/zubat")
        if response.ok:
            json_actual = response.json()
        else:
            self.fail(f"Cannot satisfy the GET request, status code {response.status_code}")

        if response.status_code == 200:
            json_expected = ExpectedJSON.translated('zubat')
        elif response.status_code == 502:  # Bad Gateway, uses standard description
            json_expected = ExpectedJSON.basic_info('zubat')
        else:
            self.fail(f"Status code {response.status_code} not handled")

        self.assertEqual(JSON.deepsort(json_expected), JSON.deepsort(json_actual), "JSON mismatch")

    def test_translated_info_normal(self) -> None:
        """
        Tests the basic info provided by pokedex for normal pokemon (neither legendary nor cave).
        """
        # Gets basic info of mewtwo
        response = requests.get(f"{self.ENDPOINT_TRANSLATED}/ditto")
        if response.ok:
            json_actual = response.json()
        else:
            self.fail(f"Cannot satisfy the GET request, status code {response.status_code}")

        if response.status_code == 200:
            json_expected = ExpectedJSON.translated('ditto')
        elif response.status_code == 502:  # Bad Gateway, uses standard description
            json_expected = ExpectedJSON.basic_info('ditto')
        else:
            self.fail(f"Status code {response.status_code} not handled")

        self.assertEqual(JSON.deepsort(json_expected), JSON.deepsort(json_actual), "JSON mismatch")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestAPI.HOST = sys.argv.pop()
        TestAPI.PORT = sys.argv.pop()
    unittest.main()
