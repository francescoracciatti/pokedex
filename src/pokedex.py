"""
This module provides the micro web server implementing the pokedex.
"""

from __future__ import annotations

import json
import logging
import sys

import requests
from flask import Flask, Response

from pokemon import Configuration, Pokemon

logging.basicConfig(format='%(asctime)s %(levelname)s %(funcName)s %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)


app = Flask(__name__)
app.config.from_object('config.Pokedex')


@app.route('/pokemon/<string:name>')
def endpoint_pokemon(name: str) -> Response:
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

    endpoint_pokeapi = app.config.get('ENDPOINT_POKEAPI')
    response = requests.get(f"{endpoint_pokeapi}/{name}")
    if response.status_code != 200:
        logging.warning(f"Cannot get basic info about {name}, status code {response.status_code}")
        return app.response_class(status=response.status_code)

    try:
        pokemon = Pokemon(response.json(), Configuration(app.config.get('LANGUAGE'), app.config.get('VERSION')))
        return app.response_class(
            response=json.dumps(pokemon.json()),
            status=200,
            mimetype='application/json'
        )
    except (KeyError, RuntimeError) as e:
        logging.error(f"Exception caught while retrieving info from json: {e}")
        return app.response_class(status=409)  # Conflict, bad resource state


@app.route('/pokemon/translated/<string:name>')
def endpoint_pokemon_translated(name: str) -> Response:
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
    response = endpoint_pokemon(name)
    if response.status_code != 200:
        logging.warning(f"Cannot get basic info about {name}, status code {response.status_code}")
        return app.response_class(status=response.status_code)

    # Translate the pokemon description
    pokemon = Pokemon(response.get_json(), Configuration(app.config.get('LANGUAGE'), app.config.get('VERSION')))

    endpoint_translation = app.config.get('ENDPOINT_POKEAPI')
    if pokemon.is_legendary or pokemon.habitat.lower() == 'cave':
        # Applies Yoda translation
        logging.info(f"Requesting Yoda translation for {name}...")
        translator = app.config.get('TRANSLATOR_YODA')
    else:
        # Applies Shakespeare translation
        logging.info(f"Requesting Shakespeare translation for {name}...")
        translator = app.config.get('TRANSLATOR_SHAKESPEARE')

    response = requests.post(f"{endpoint_translation}/{translator}", data={'text': pokemon.description})

    if response.status_code != 200:
        logging.info(f"Cannot translate description, status code {response.status_code}")
        return app.response_class(
            response=json.dumps(pokemon.json()),
            status=response.status_code,
            mimetype='application/json'
        )

    try:
        pokemon.description = response.json()['contents']['translated']
        response = app.response_class(
            response=json.dumps(pokemon.json()),
            status=200,
            mimetype='application/json'
        )
        return response
    except KeyError as e:  # Return basic info
        logging.error(f"Got exception while looking for the translated text, {e}")
        return app.response_class(
            response=json.dumps(pokemon.json()),
            status=200
        )


if __name__ == '__main__':
    """
    Entry point, starts the web server.
    """
    logging.info("Pokedex is running...")

    app.config.from_object('config.Pokedex')

    host = app.config.get('HOST')
    port = app.config.get('PORT')

    # Current args override the web server configuration
    if len(sys.argv) > 1:
        host = sys.argv.pop()
        port = int(sys.argv.pop())
        logging.info(f"Overriding configuration with host {host} and port {port}")

    app.run(host=host, port=port)

    logging.info(f"Done, going to sleep in my pokeball")
