"""
Web server configuration parameters.
"""

class Pokedex(object):
    """
    Configuration parameters.
    """
    LANGUAGE = 'en'
    VERSION = 'red'

    # PokeApi endpoint, used to gather info about pokemon.
    ENDPOINT_POKEAPI = 'https://pokeapi.co/api/v2/pokemon-species'

    # FunTranslations endpoint and translators, used to translate the description of the pokemon.
    ENDPOINT_TRANSLATIONS = 'https://api.funtranslations.com/translate'

    TRANSLATOR_YODA = 'yoda.json'
    TRANSLATOR_SHAKESPEARE = 'shakespeare.json'
