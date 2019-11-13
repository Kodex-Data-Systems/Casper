# Settings
## Example settings.json
* Create settings.json in rootdir
```json
{
   "version": "0.0.3",
   "node": "http://localhost:3101",
   "platform": "Darwin-15.6.0-x86_64-i386-64bit",
   "dbpath": "accounts.db",
   "genesis": "c63a07f3e0db52c9abf886453316a1698d41a77023972c708345acf6645a8c0c",
   "cryptomodule": "Fernet",
   "jmpath": "/tmp/jormungandr"
}
```

# Usage
## Run Setup
* or run `python3 config` or `yarn setup` to create a config file

## Run CLI UI
* `python3 .` or `npm run casper` or `yarn casper`

## Depencies
* Python 3.6+
* pip3 install db-sqlite3
* pip3 install pprint
* pip3 install requests
* pip3 install cryptography
* pip3 install tabulate

**Optional Crypt Package:**
* pip3 install pycrypto
