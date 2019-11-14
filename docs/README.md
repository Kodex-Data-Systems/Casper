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

After running setup a `settings.yaml` file will be produced, similar to the following:


```yaml
version: 0.0.3
node: localhost:3101
platform: Darwin-18.7.0-x86_64-i386-64bit
dbpath: config/accounts.db
genesis: 0c6db1bc6b4794c8d3913529ebe6ba986684c3b23bfe4879fde37dabbc71ba93
cryptomodule: Fernet
jmpath: /tmp/jormungandr
```
## Depencies
* Python 3.6+
* pip3 install db-sqlite3
* pip3 install pprint
* pip3 install requests
* pip3 install cryptography
* pip3 install ruamel.yaml
* pip3 install tabulate

## Optional requirements
* sudo apt-get install python3-dev
* sudo yum install python-devel (CentOS)

**Optional Cryptography Package:**
* pip3 install pycrypto

# Usage

## Run CLI UI
* `python3 .` or `npm run casper` or `yarn casper`

## Run Setup
* or run `python3 config` or `yarn setup` to create a config file

# [Casper Module Documentation](casper.md)
