"""
This module provides the standard model for pokemon.
"""

from __future__ import annotations

from typing import Dict, Any, Optional

from src.utils.utils import replace_escape


class Configuration(object):
    """
    Wraps config variables.
    """

    def __init__(self, language: str, version: str) -> None:
        self.language = language
        self.version = version


class Pokemon(object):
    """
    Stores the pokedex configuration.
    """

    @staticmethod
    def retrieve_description(json: Dict[Any, Any], configuration: Configuration) -> Optional[str]:
        """
        Gets the description of the pokemon from the given json.

        :param json: the json containing the description of the pokemon
        :param configuration: the configuration parameters that drive the information retrieval
        :return: the description of the pokemon if available for the current language and version, otherwise None
        """
        entries = json['flavor_text_entries']
        for e in entries:
            # Looks for the current language and version
            if e['language']['name'] == configuration.language and e['version']['name'] == configuration.version:
                return replace_escape(e['flavor_text'])
        return None

    @classmethod
    def build_from_pokeapi_json(cls, pokeapi_json: Dict[Any, Any], configuration: Configuration) -> Pokemon:
        """
        Builds a pokemon from the pokeapi json response.

        :param pokeapi_json: the json containing the description of the pokemon
        :param configuration: the configuration parameters
        """
        json = {
            "name": pokeapi_json['name'],
            "description": cls.retrieve_description(pokeapi_json, configuration),
            "habitat": pokeapi_json['habitat']['name'],
            "isLegendary": pokeapi_json['is_legendary']
        }
        return Pokemon(json)

    def __init__(self, json: Dict[str, Any]) -> None:
        """
        Builds the pokemon from a json containing its description.

        :param json: the json containing the description of the pokemon
\        """
        self.name = json['name']
        self.description = json['description']
        self.habitat = json['habitat']
        self.is_legendary = json['isLegendary']

    def json(self) -> Dict[str, Any]:
        """
        Jsonifies the pokemon.

        :return: the dict representing the pokemon
        """
        return {
            "name": self.name,
            "description": self.description,
            "habitat": self.habitat,
            "isLegendary": self.is_legendary
        }
