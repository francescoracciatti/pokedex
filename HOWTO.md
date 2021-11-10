# How To
- [Run](#run)
- [Change Host/Port](#change-hostport)
- [Change Language/Version](#change-languageversion)
- [Test](#test)

# Run
You can run Pokedex either via Docker or via Terminal. 
Refer [README::Running](README.md#running)

# Change Host/Port
If you want to set a custom host and port like 192.168.0.1:6000, you can do the following.

## Docker 
Edit the `CMD` line at the end of the Dockerfile.
```dockerfile
CMD ["flask", "run", "--host", "192.168.0.1", "--port", "6000"]
```
Set the host and the port you prefer.
Then build the image and run the container.
```shell
$ cd path_to/pokedex
$ docker build --tag pokedex .
$ docker run -p 6000:6000 pokedex
```

Alternatively, if you want to change only the port Docker exposes to your local machine,
you can simply change the `publish` parameter withouth changing the Dockerfile. 
```shell
$ docker run -p 6000:5000 pokedex
```

## Terminal
Specify the host and port you prefer when running pokedex.
```shell
$ cd path_to/pokedex/src
$ flask run --host 192.168.0.1 --port 6000
```

# Change Language/Version
To change the language/version of the Pokedex web server, 
edit the entries `LANGUAGE`/`VERSION` in [config.py](config.py).
```python
class Pokedex(object):
    """
    Web server configuration parameters.
    """
    HOST = '0.0.0.0'
    PORT = 5000

    LANGUAGE = 'fr'
    VERSION = 'black'
```

You can find the available languages [here](https://pokeapi.co/api/v2/language/). \
You can find the available versions [here](https://pokeapi.co/api/v2/version/).


## Test
When the web server runs, you can make API calls via Web Browser or terminal.

If you prefer the terminal, you may think to use [httpie](https://httpie.io/).
