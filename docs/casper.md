# CasperCore

```py
import json
from casper import CasperCore
with open('settings.json', 'r') as json_file:
    settings = json.load(json_file)

casper = CasperCore(settings, input("Your Password"))
```

## casper.db

```py
class Database(object):
    def __init__(self, settings, USER_PWD, module="Fernet"):
```
- - -

### `db.all_acct()`
**RETURNS ARRAY**
* id `int`
* addr `str`
* secret `str`
* public `str`
- - -

### `db.get_acct_by_id(id)`
**RETURNS**
* id `int`
* addr `str`
* secret `str`
* public `str`
- - -

### `db.save_acct(**params)`
**Parameters:**
* secretKey
* publicKey
* accountAddress

- - -

## casper.node
```py
class Node(object):
    def __init__(self, settings):
        self.url = settings["node"]
        # Checkin an ApiRoute to ensure node is up
        try:
            response_code = urllib.request.urlopen(f"{self.url}/api/v0/network/stats").getcode()
        except:
            # here we can determine response_code, but not neccesary yet
            print(f"ERROR NODE IS NOT RESPONDING")
            sys.exit(2)

```
- - -

### `node.show_peers()`
* runs `netstat -an | grep jormungandr | grep ESTABLISHED`
- - -

### `node.show_node_stats()`
```py
def show_node_stats(self):
    return self._get(f"{self.url}/api/v0/node/stats")
```

**RETURNS**
```json
{
   "state":"Running",
   "blockRecvCnt":751,
   "lastBlockDate":"5.296",
   "lastBlockFees":0,
   "lastBlockHash":"bdb7b5af37250fe8ed96dd45cbf31de5b92ad9e1ed479d8bf86cbbfa5b472314",
   "lastBlockHeight":"581",
   "lastBlockSum":0,
   "lastBlockTime":"2019-11-07T23:43:28+00:00",
   "lastBlockTx":0,
   "txRecvCnt":57,
   "uptime":9544
}
```
- - -

### `node.show_stake()`
```py
def show_stake(self):
    return self._get(f"{self.url}/api/v0/stake")
```

**RETURNS**
```json
{
   "epoch":5,
   "stake":{
      "dangling":0,
      "pools":[
         ["6edf2e3c419f506139be3c6390e35ea8e095438f896603767cdf27847bb9311c",1000000433],
         ["51bdc254d1cc2e3c590afd0b8e7f7b3cdeeebfb29173fa9c704d3288ee5e9ce2", 1000000000]
      ],
      "unassigned":96999998167
   }
}
```
- - -

### `node.show_stake_pools()`
```py
def show_stake_pools(self):
    return self._get(f"{self.url}/api/v0/stake_pools")
```

**RETURNS**
```json
[
   "6edf2e3c419f506139be3c6390e35ea8e095438f896603767cdf27847bb9311c",
   "51bdc254d1cc2e3c590afd0b8e7f7b3cdeeebfb29173fa9c704d3288ee5e9ce2",
   "2b81171edf761b1367e27e31398db940111d76d0c0f47ad4037145e10b77d495",
   "931c55377993b797034b27a659e3f8cb093e0b798e01679e1eaab0d900a5f8a5",
   "3827efb21ef23fea36c9405ce65700cdd6a058a091b2ac650c701db4cfe04e01",
   "819021fcbdbc3a38676ff5e450d24ec275f7b2b60b51c1caae6c9009a20053c9",
   "ff58b1eec899c8c07e19e045189f0b6731dd90411dd191594f12a1251b413611",
   "8baac4f01c784de9f5bfb5ca03e3879ec55c81b7eb302a3fd2c7a18319111d2c",
   "25fee93433d5b7d9e49eb67109448b1a563078206ee8b5d5249b7d2487321674",
   "b27eeffc572382f62c977ef3af924be0b3ffe7041306ce4f50ef013f0742abcd",
   "499e2bcd1474eede48ed6d70dd0401bf1e5b302c6623296f997003e489d36a3b"
]
```
- - -

### `node.show_stats()`
```py
def show_stats(self):
    return self._get(f"{self.url}/api/v0/network/stats")
```

**RETURNS**
```json
[
   {
      "establishedAt":"2019-11-07T21:21:32.346585898+00:00",
      "lastBlockReceived":"2019-11-07T23:36:43.026355855+00:00",
      "lastFragmentReceived":"2019-11-07T23:31:28.404545896+00:00",
      "lastGossipReceived":"2019-11-07T23:36:42.301722844+00:00",
      "nodeId":"eb55d9a20d929299147125049451700b37973c60c088b3d6"
   },
   ...
]
```
- - -

## casper.cli
```py
class Cli(object):
    def __init__(self, settings):
        self.node = settings["node"]
        self.storage = settings["jmpath"]
        self.loaded = True
        self.genesis = settings["genesis"]
        if "NO_JORMUNGANDR" in settings:
            self.no_jormungandr = settings["NO_JORMUNGANDR"]
        else:
            self.no_jormungandr = False
```
- - -

### `cli.create_pool(**params)`
**PARAMS:**
* pk `str`
* sk `str`
* account `str`

**RETURNS:**
* node_id `str`

**EXAMPLE**
```py
if choice == '4': #  Create Stake Pool
    account = self.account[1]
    secret = self.account[2]
    public = self.account[3]
    casper.cli.create_pool(public, secret, account)
```
- - -

### `cli.create_delegation_certificate(**params)`
**PARAMS:**
* pool_id `str`
* pk `str`
* sk `str`
* account `str`

**RETURNS:**
* fragment_id `str`
* cert_id `str`
* signed_id `str`

**EXAMPLE**
```py
if choice == '5': #  Delegate Stake Pool
    if self.account is not None:
        pool = input('Enter Stake Pool: ')
        account = self.account[1]
        public = self.account[3]
        secret = self.account[2]
        self.clear()
        casper.cli.create_delegation_certificate(pool, public, secret, account)
```
- - -

### `cli.create_acct()`
**RETURNS:**
* secret `str`
* public `str`
* acct `str`

**EXAMPLE**
```py
  secret, public, acct = casper.cli.create_acct()
```
- - -

### `cli.acct_by_secret(**params)`
**PARAMS**
* secret `str`

**RETURNS:**
* secret `str`
* public `str`
* acct `str`

**EXAMPLE**
```py
  secret, public, acct = casper.cli.acct_by_secret()
```
- - -

### `cli.prefix(prefix, priv_key) -> str`
**PARAMETERS**
* prefix `str`
* priv_key `str`

**EXAMPLE**
```py
  secret, public, acct = casper.cli.create_acct()
  prefixed = casper.cli.prefix("CASPERT", secret)
```
- - -

### `cli.show_jcli_version() -> str`
**VERSION STRING**
```
jcli 0.5.6+lock (master-d505e9d5, release, macos [x86_64]) - [rustc 1.38.0 (625451e37 2019-09-23)]
```
- - -

### `cli.show_jormungandr_version() -> str`
**VERSION STRING**
```
jormungandr 0.5.6+lock (master-d505e9d5, release, macos [x86_64]) - [rustc 1.38.0 (625451e37 2019-09-23)]
```
- - -

### `cli.show_blockchain_size() -> str`
**SIZE STRING**
- - -

### `cli.show_stake()`
**RETURNS**
```json
{
    "epoch": 96,
    "stake": {
        "dangling": 0,
        "pools": [
            ["e0362613ecf5dba1b322481228a623285349b5f42c9dcaf1057faaf10a36d172",
                0
            ],
            ["f89a43e886c33db5b36e4dcdd28f631b4b7b12a74b64d025421655a52903fbd4",
                0
            ],
            ["113aa229c02d1daf3f56808ea34f52c05ac8fa188f9dda1f3cecddfaeda5ec64",
                0
            ]
        ],
        "unassigned": 79998158092
    }
}
```
- - -

### `cli.show_stake_pools()`
**RETURNS**
```json
[
  "ada97ef04167d88fabf978f264e64fa880ef681068335d5a2c22fa87f4d4dba5",
  "5a77b8cc66322840d3443bebd2a609601385c92bc83165ea59066443f6ee41e9",
  "6edf2e3c419f506139be3c6390e35ea8e095438f896603767cdf27847bb9311c",
  "51bdc254d1cc2e3c590afd0b8e7f7b3cdeeebfb29173fa9c704d3288ee5e9ce2",
  "cab0df8f1fa0889ff77e1096338a27fa38c8c8cfbebbb86c8f9c44738ac8b702",
  "2b81171edf761b1367e27e31398db940111d76d0c0f47ad4037145e10b77d495"
]
```
- - -

### `cli.show_balance(acct_addr)`
**ERROR IF 0 BALANCES**
```
failed to make a REST request
  |-> node rejected request because of invalid parameters
  |-> http://localhost:3101/api/v0/account/59c5860c6410e47fc08092639cd006be8133f272d3eccc327a155e0c0fe889b8: Client Error: 404 Not Found
Unable to view balance, account has not yet received a tx or node is offline.
list index out of range
0
```
**RETURNS**
* acct_addr `str`
* balance `str`
* balance `str`
* counter `int`
* pools List(addr `str`)
- - -

### `cli.send_single_tx(**params)`
**Parameters:**
* amount
* sender
* reciever
* secret
* nonce

```py
sender = self.account[1]
secret = self.account[2]
amount = int(input('Enter Send Amount: '))
receiver = input('Receiver: ')
self.clear()
casper.cli.send_single_tx(
    amount,
    sender,
    receiver,
    secret
)
```
- - -

### `cli.send_multiple_tx(**params)`
**Parameters:**
* amount
* sender
* reciever
* secret
* rounds
* await_each

```py
sender = self.account[1]
secret = self.account[2]
amount = int(input('Enter Send Amount: '))
receiver = input('Receiver: ')
rounds = input("Send Single Transaction (Y/n): ").lower()
self.clear()
rounds = int(input("Enter Number Of Cycles: "))
casper.cli.send_multiple_tx(
    amount,
    sender,
    receiver,
    secret,
    rounds,
    False
)
```
- - -

# [Home](README.md)
