# Casper
A simple tool for interacting with the Cardano blockchain

Casper requires a Jormungandr node running locally. You can edit the `config.py` to reflect your REST API.

Sample config.py:
```
NODE = "http://127.0.0.1:3101"
STORAGE = "/tmp/jormungandr"
```
To use:

`python3 casper.py`
