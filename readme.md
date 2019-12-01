# Casper

Casper is an open source library designed to improve access to the Jormungandr node client through JCLI, developed by Kodex Data Systems.

# Settings

# Usage
## Run CLI UI
* `python3 .` or `npm run casper` or `yarn casper`

## Run Setup
* or run `python3 config` or `yarn setup` to create a config file

## Example settings.yaml
* Create settings.yaml in `./config`

```yaml
version: 0.0.4
node: localhost:3101
platform: Darwin-18.7.0-x86_64-i386-64bit
dbpath: config/accounts.db
genesis: 0c6db1bc6b4794c8d3913529ebe6ba986684c3b23bfe4879fde37dabbc71ba93
cryptomodule: Fernet
jmpath: /tmp/jormungandr
```

## Dependencies
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

**Optional Crypt Package:**
* pip3 install pycrypto


If you find this software useful, consider buying us a beer using [Yoroi](web+cardano:Ae2tdPwUPEZFowK1DYUa1WxpQFCr1zZyLwcfrSeiuPKb4NSXDpJALxBzTeK?amount=100.000000) to show your support!

<web+cardano:Ae2tdPwUPEZFowK1DYUa1WxpQFCr1zZyLwcfrSeiuPKb4NSXDpJALxBzTeK?amount=100.000000>


* Our ADA donation address is: Ae2tdPwUPEZFowK1DYUa1WxpQFCr1zZyLwcfrSeiuPKb4NSXDpJALxBzTeK

* Our BTC donation address is: bc1qdfspmlkcp094zws0gwqy2d086sldxlehdrln9m

* Our ETC donation address is: 0x9Cc9201c47f4ff4b78d8b4Fd1891E3dA02E155B6