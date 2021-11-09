# Pokedex
Pokedex is a micro web server that provides public endpoints to gather information about Pokemon.

![test gif](doc/gif/test-capture.gif)

Pokedex is implemented in Python3 + Flask and relies on:
 - [PokéApi](https://pokeapi.com)
 - [FunTranslations](https://funtranslations.com)

## Running
By default, the web server runs at `0.0.0.0/5000`. 

### Docker
```shell
$ cd path_to/pokedex
$ docker run -p 5000:5000 pokedex
```

### Terminal
Initialize a new venv and install the [requirements](requirements.txt), then:
```shell
$ cd path_to/pokedex/src
$ export FLASK_APP=pokedex
$ flask run
 ```
You can specify the host and port by editing the configuration file [pokedex/src/config.ini](src/config.ini).


## Endpoints
### Basic Pokemon Information
```
/HTTP/GET /pokemon/<pokemon name>
```
Given a Pokemon name, this endpoint returns its:
 - name,
 - standard description,
 - habitat,
 - legendary status.

Example call and API response:
```
http://localhost:5000/pokemon/mewtwo
```
```json
{
  "name": "mewtwo",
  "description": "It was created by a scientist after years of horrific gene splicing and DNA engineering experiments.",
  "habitat": "rare",
  "isLegendary": "true"
}
```

### Translated Pokemon Description
```
/HTTP/GET /pokemon/translated/<pokemon name>
```
Given a Pokemon name, this endpoint returns its:
 - name,
 - translated description,
 - habitat,
 - legendary status.
 
The description is translated by using:
 - the Yoda translator, if the Pokemon's habitat is `cave`or if it is `legendary`;
 - the Shakespeare translator, otherwise.

If the translation service is not available, it uses the standard description.  
 
Example call and API response:
```
http://localhost:5000/pokemon/translated/mewtwo
```
```json
{
  "name": "mewtwo",
  "description": "Created by a scientist after years of horrific gene splicing and DNA engineering experiments, it was.",
  "habitat": "rare",
  "isLegendary": "true"
}
```

## Author
Francesco Racciatti

## License
This project is licensed under the [MIT license](LICENSE).
