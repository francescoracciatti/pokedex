"""
This module provides the standard model for pokemon.
"""

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

    def __init__(self, json: Dict[Any, Any], configuration: Configuration) -> None:
        """
        Stores the description of the pokemon.

        :param json: the json containing the description of the pokemon
        :param configuration: the configuration parameters
        """
        self.name = json['name']
        self.description = self.retrieve_description(json, configuration)
        self.habitat = json['habitat']['name']
        self.is_legendary = json['is_legendary']

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
