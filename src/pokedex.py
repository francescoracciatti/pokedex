"""
This module provides the micro web server implementing the pokedex.
"""

import logging

from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/pokemon/<string:name>')
def pokemon(name: str):
    logging.info(f"Got {name}")
    return jsonify({
        "name": "mewtwo",
        "description": "It was created by a scientist after years of horrific gene splicing "
                       "and DNA engineering experiments.",
        "habitat": "rare",
        "isLegendary": True
    })


@app.route('/pokemon/translated/<string:name>')
def translated(name: str):
    logging.info(f"Got {name}")
    return jsonify({
        "name": "mewtwo",
        "description": "It was created by a scientist after years of horrific gene splicing "
                       "and DNA engineering experiments.",
        "habitat": "rare",
        "isLegendary": True
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
