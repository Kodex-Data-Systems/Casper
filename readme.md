## Docs

For full documentation
```
cd Casper
docsify serve ./docs
```


# Settings
## Example settings.json
* Create settings.json in rootdir
```json
{
   "version": "0.0.2",
   "node": "http://localhost:3101",
   "dbpath": "accounts.db",
   "genesis": "c63a07f3e0db52c9abf886453316a1698d41a77023972c708345acf6645a8c0c",
   "cryptomodule": "Fernet",
   "jmpath": "/tmp/jormungandr"
}
```

# Usage
## Run Setup
* or run `python3 setup_casper.py` or `yarn setup` to create a config file

## Run CLI UI
* `python3 casper.py` or `npm run casper` or `yarn casper`

## Dependencies
* Python 3.6+
* pip3 install db-sqlite3
* pip3 install pprint
* pip3 install requests
* pip3 install cryptography
* pip3 install tabulate

**Optional Crypt Package:**
* pip3 install pycrypto
