"""
This module provides the micro web server implementing the pokedex.
"""

from __future__ import annotations

import configparser
import json
import logging
import sys
from typing import Dict, Any, Optional

import requests
from flask import Flask, jsonify, Response

logging.basicConfig(format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)

app = Flask(__name__)

HTML_ESCAPE_SEQUENCES = ['\f', '\r', '\n', '\t']


def replace_escape(msg: str, substr: str = ' ') -> str:
    """
    Replaces the HTML escape sequences in the given message with the given substr.

    :param msg: the message
    :param substr: the replacing substr
    :return: the message with no HTML escape sequences
    """
    replaced = msg
    for e in HTML_ESCAPE_SEQUENCES:
        replaced = replaced.replace(e, substr)
    return replaced


class Pokedex(object):
    """
    Stores the pokedex configuration.
    """

    language = 'en'
    version = 'red'

    @classmethod
    def get_description(cls, json: Dict[Any, Any]) -> Optional[str]:
        """
        Gets the description of the pokemon from the given json.

        :param json: the json containing the description of the pokemon
        :return: the description of the pokemon if available for the current language and version, otherwise None
        """
        entries = json['flavor_text_entries']
        for e in entries:
            # Looks for the current language and version
            if e['language']['name'] == cls.language and e['version']['name'] == cls.version:
                return replace_escape(e['flavor_text'])
        return None


# Public PokeApi's endpoint used to gather info about pokemon
ENDPOINT_POKEAPI = 'https://pokeapi.co/api/v2/pokemon-species'

# Public FunTranslations' endpoint used to translate descriptions
ENDPOINT_TRANSLATIONS = 'https://api.funtranslations.com/translate'
TRANSLATOR_YODA = 'yoda.json'
TRANSLATOR_SHAKESPEARE = 'shakespeare.json'


@app.route('/pokemon/<string:name>')
def pokemon(name: str) -> Response:
    """
    Endpoint /HTTP/GET /pokemon/<pokemon name>

    Given a Pokemon name, this endpoint returns its:
     - name,
     - standard description,
     - habitat,
     - legendary status.

    :param name: the name of the pokemon
    :return: the json containing the basic info of the given pokemon
    """
    logging.warning(f"Requesting basic info about {name} ...")
    response = requests.get(f"{ENDPOINT_POKEAPI}/{name}")
    if response.status_code != 200:
        logging.warning(f"Cannot get basic info about {name}, status code {response.status_code}")
        return app.response_class(status=response.status_code)

    info = response.json()

    try:
        data = {
            "name": info['name'],
            "description": Pokedex.get_description(info),
            "habitat": info['habitat']['name'],
            "isLegendary": info['is_legendary']
        }
        return app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json'
        )
    except (KeyError, RuntimeError) as e:
        logging.error(f"Exception caught while retrieving info from json: {e}")
        return app.response_class(status=409)  # Conflict, bad resource state


@app.route('/pokemon/translated/<string:name>')
def translated(name: str):
    """
    Endpoint /HTTP/GET /pokemon/translated/<pokemon name>

    Given a Pokemon name, this endpoint returns its:
     - name,
     - translated description,
     - habitat,
     - legendary status.

    The description is translated by using:
     - the Yoda translator, if the Pokemon's habitat is `cave`or if it is `legendary`;
     - the Shakespeare translator, otherwise.

    If the translation service is not available, it uses the standard description.

    :param name:
    :return:
    """
    # Get basic info
    response = pokemon(name)
    if response.status_code != 200:
        logging.warning(f"Cannot get basic info about {name}, status code {response.status_code}")
        return app.response_class(status=response.status_code)

    # Translate the pokemon description
    basic_info = response.get_json()
    if basic_info['isLegendary'] or basic_info['habitat'].lower() == 'cave':
        # Applies Yoda translation
        logging.info(f"Requesting Yoda translation for {name}...")
        response = requests.post(f"{ENDPOINT_TRANSLATIONS}/{TRANSLATOR_YODA}", data={'text': basic_info['description']})
    else:
        # Applies Shakespeare translation
        logging.info(f"Requesting Shakespeare translation for {name}...")
        response = requests.post(f"{ENDPOINT_TRANSLATIONS}/{TRANSLATOR_YODA}", data={'text': basic_info['description']})

    if response.status_code != 200:
        logging.info(f"Cannot translate description, status code {response.status_code}")
        return app.response_class(
            response=json.dumps(basic_info),
            status=response.status_code,
            mimetype='application/json'
        )

    try:
        translated_info = basic_info
        translated_info['description'] = response.json()['contents']['translated']
        response = app.response_class(
            response=json.dumps(translated_info),
            status=200,
            mimetype='application/json'
        )
        return response
    except KeyError as e:
        logging.error(f"Got exception while looking for the translated text, {e}")
        return app.response_class(
            response=json.dumps(basic_info),
            status=200
        )


if __name__ == '__main__':
    """
    Entry point, starts the web server.
    """
    logging.info("Pokedex is running...")

    # Reads the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Gets the web server configuration
    host = config['WebServer']['host']
    port = config['WebServer']['port']
    logging.info(f"Web server configuration host {host} and port {port}")

    # Gets the pokedex configuration
    Pokedex.language = config['Pokedex']['language']
    Pokedex.version = config['Pokedex']['version']

    # Current args override the web server configuration
    if len(sys.argv) > 1:
        host = sys.argv.pop()
        port = int(sys.argv.pop())
        logging.info(f"Overriding configuration with host {host} and port {port}")

    app.run(host=host, port=port)

    logging.info(f"Done, going to sleep in my pokeball")
