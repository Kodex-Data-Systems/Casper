# Introduction

Casper is a simple, but powerful, blockchain interface tool designed to be used in conjunction with a Jormungandr node client and JCLI.  

**Features:**
* Non-Custodial Storage
* Encrypted Wallets by Default
* Private Transaction Queries
* No Data Surveillance

# Getting Started

## Yarn Setup

Run `yarn setup` to load the configuration utility.  You will be prompted to enter your local settings, or use defaults, as described below.


```ascii

Welcome to Casper Setup.

You can press Enter at any prompt to use the
following default Settings, or enter your own.

  REST API SERVER:  http://localhost:3101
  Database Storage Path:  ./accounts.db
  Genesis Hash:  bad49dbbd149ee6cbe1f172d4a727b5e3cf9ea057651f303758eff9cb6ce8387
  Crypto Module:  Fernet is default, PyCrypto is the alternative.
  Blockchain Storage Path:  /tmp/storage



```

After running setup a `settings.json` file will be produced, similar to the following:


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
## Dependencies
* Python 3.6+
* pip3 install db-sqlite3
* pip3 install pprint
* pip3 install requests
* pip3 install cryptography
* pip3 install tabulate

**Optional Cryptography Package:**
* pip3 install pycrypto

# Usage
## Run Setup
* or run `python3 setup_casper.py` or `yarn setup` to create a config file

## Run CLI UI
* `python3 casper.py` or `npm run casper` or `yarn casper`



# [Casper Module Documentation](casper.md)
