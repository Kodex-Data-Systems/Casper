import sys, subprocess, time, pprint, os, getpass, json
from tabulate import tabulate

from casper import CasperCore
from casper.utils import verify_password, parse_yaml, Yaml, date_crop
from janalyze import JAnalyze
# os.environ["PYTHONIOENCODING"] = "utf-8"
yaml = Yaml()
_MENU = """
Please choose an option:

(1) Create New Testnet Address   (2) Import Existing Address  (3) Load Address
(4) Create Stake Pool            (5) Delegate Stake           (6) Send Transaction
(7) Display Current Address      (8) Check Balance            (9) Show All Accounts

(10) Show Message Log            (11) Show Node stats         (12) Show Established Peers
(13) Show Stake Pools            (14) Show Stake              (15) Show Blockchain Size
(16) Show Leader Logs            (17) Show Settings           (18) Aggregate Blocks Produced
(19) Stake Distribution          (20) Genesis Decode          (21) Fork Check

(e) Export All Accounts          (i) Import accounts.yaml     (f) View Config File
(v) Show Versions                (c) Clear Screen             (q) Quit

"""

if os.path.exists("config/settings.yaml") is False:
    exec(open("config/__main__.py").read(), globals())
    print("\n\nSTARTING CASPER")

settings = parse_yaml("config/settings.yaml", file=True)

if "userpwd" in settings:
    #  saving password in settings file is only thought for dev mode
    #  use on your own risk
    _USER_PWD = settings["userpwd"]
else:
    _USER_PWD = getpass.getpass("Enter your Password: ")


if "cryptomodule" in settings:
    _DEFAULT_CRYPTO = settings["cryptomodule"]
else:
    _DEFAULT_CRYPTO = input("ENTER CRYPT MODULE (Fernet, PyCrypto, RAW): ")
    if _DEFAULT_CRYPTO is "RAW":
        _DEFAULT_CRYPTO = None

cspr = CasperCore(settings, USER_PWD=_USER_PWD, CRYPTO_MOD=_DEFAULT_CRYPTO)
analyze = JAnalyze(settings)

class CliInterface:
    @classmethod
    def typed_text(cls, string, sleep_time, pause=0.5):
        cls.string = string
        cls.sleep_time = sleep_time
        cls.pause = pause
        ''' Mimic human typing '''
        for letter in cls.string:
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(cls.sleep_time)
        time.sleep(cls.pause)
        print("\n\n")

    def __init__(self):
        self.end_loop = False
        self.account = None

        self.typed_text('CASPER CLI UI v1.2 -- Kodex Data Systems 2019', 0.004)
        print('\n\n')

    def determine_status(self, log):
        if "Rejected" in log["status"]:
            _status = log["status"]["Rejected"]["reason"]
        elif "InABlock" in log["status"]:
            blockhash = log["status"]["InABlock"]["block"]
            _status = blockhash[:-20] + "..."
        elif "Pending" in log["status"]:
            _status = "Pending"
        elif "Block" in log["status"]:
            _status = (log["status"]["Block"]["block"], log["status"]["Block"]["chain_length"])
        else:
            _status = "UNKNOWN"
        return _status

    def clear(self):
        cls_platforms = ["linux", "linux2", "darwin"]
        if sys.platform == 'win32':
            subprocess.call('cls', shell=True)
        elif sys.platform in cls_platforms:
            subprocess.call('clear', shell=True)
        else:
            self.typed_text('Command not compatible with your OS', 0.002)

    def save_acct_by_secret(self, _sk):
        try:
            secret, public, address = cspr.cli.acct_by_secret(_sk)
            cspr.db.save_acct(secret, public, address)
            self.typed_text(f'Account Added: {address}', 0.002)
        except:
            print("IMPORT ERROR")

    def run(self):
        while not self.end_loop:
            print(_MENU)
            choice = input('Your Choice: ')

            if choice == '1':  # Create.
                self.clear()
                _sk, _pk, _ak = cspr.cli.create_acct()
                cspr.db.save_acct(_sk, _pk, _ak)
                self.typed_text(f'Account Created: {_ak}', 0.002)

            if choice == '2':  # Import existing.
                self.clear()
                _sk = input("Input Secret Key: ")
                self.save_acct_by_secret(_sk)

            if choice == '3':  # Load.
                self.clear()
                myaccounts = cspr.db.all_acct()
                if myaccounts is not None:
                    for acct in myaccounts:
                        print(acct[0], acct[1])

                    _id = input("\nSelect Acount Number: ")
                    try:
                        _selected = cspr.db.get_acct_by_id(int(_id))
                        if _selected is not None:
                            self.typed_text(f'Account Loaded: {_selected[1]}', 0.002)
                            self.account = _selected
                            self.clear()
                        else:
                            print("Account Not In Database")
                    except:
                        self.typed_text(f'Account Not In List', 0.002)

            if choice == '4': #  Create Stake Pool
                self.clear()
                if self.account is not None:
                    pool_name = input('Enter the pool name: ')
                    account = self.account[1]
                    secret = self.account[2]
                    public = self.account[3]
                    print('\nStake Pool ID')
                    print('-' * 33)
                    cspr.cli.create_pool(public, secret, account, pool_name)

                else:
                    print("You Need To Load An Account First")

            if choice == '5': #  Delegate Stake Pool
                self.clear()
                if self.account is not None:
                    pool = input('Enter Stake Pool: ')
                    account = self.account[1]
                    public = self.account[3]
                    secret = self.account[2]
                    self.clear()
                    tx = cspr.cli.create_delegation_certificate(pool, public, secret, account)
                    print(f"Delegation Fragment: {tx[0]}")

                else:
                    print("You Need To Load An Account First")

            if choice in ("6", "tx"):  # Send Tx.
                self.clear()
                if self.account is not None:
                    sender = self.account[1]
                    secret = self.account[2]
                    amount = int(input('Enter Send Amount: '))
                    receiver = input('Receiver: ')
                    rounds = input("Send Single Transaction (Y/n): ").lower()
                    if rounds == "y":
                        self.clear()
                        cspr.cli.send_single_tx(
                            amount,
                            sender,
                            receiver,
                            secret
                        )
                    else:
                        self.clear()
                        rounds = int(input("Enter Number Of Cycles: "))
                        cspr.cli.send_multiple_tx(
                            amount,
                            sender,
                            receiver,
                            secret,
                            rounds,
                            False
                        )

                else:
                    print("You Need To Load An Account First")

            if choice == '7':  # Display current.
                self.clear()
                if self.account is None:
                    print("No Account Loaded")
                else:
                    print(f'Loaded Account: {self.account}')

            if choice in ("8", "b"):
                self.clear()
                if self.account is None:
                    print("No Account Loaded")
                else:
                    try:
                        addr, balance, nonce, pools = cspr.cli.show_balance(
                            self.account[1],
                            raw=False
                        )
                        print(f"Address: {addr}\nBalance: {balance}\nNonce: {nonce}")
                        c = 0
                        if len(pools) > 0:
                            for pool in pools:
                                c = c + 1
                                print(f"POOL {c}: {pool[0]} || WEIGHT: {pool[1]}")
                    except:
                        print("0")

            if choice == "9": # Show all accounts
                self.clear()
                pprint.pprint(cspr.db.all_acct())

            if choice in ("10", "m"): # Message log.
                self.clear()
                message_logs = []
                for log in cspr.cli.message_logs():
                    message_logs.append({
                        "fragment_id": log["fragment_id"],
                        "last_updated_at": date_crop(log["last_updated_at"]),
                        "received_at": date_crop(log["received_at"]),
                        "received_from": log["received_from"],
                        "status": self.determine_status(log)
                    })

                header = message_logs[0].keys()
                rows =  [x.values() for x in message_logs]
                table = tabulate(rows, header, tablefmt="psql")
                print(table)

            if choice == '11': # Node stats.
                self.clear()
                pprint.pprint(cspr.node.show_node_stats())

            if choice == '12': #  Show Peers.
                self.clear()
                pprint.pprint(cspr.node.show_peers())

            if choice == '13': #  Show Stake Pools.
                self.clear()
                pools = cspr.node.show_stake_pools()

                pprint.pprint(pools)
                print("\n\n")
                self.typed_text(f'Number of registered pools: {str(len(pools))}', 0.004)

            if choice == '14': #  Show Stake.
                self.clear()
                stake = cspr.node.show_stake()["stake"]["pools"]
                table = tabulate(
                    stake,
                    headers=[
                        "Hex-encoded stake pool ID",
                        "Total pool value"
                    ],
                    tablefmt="psql"
                )
                print(table)

            if choice == '15': #  Show Chain Size.
                self.clear()
                pprint.pprint(cspr.cli.show_blockchain_size())

            if choice == '16': #  Show Leaders Logs.
                self.clear()
                #  pprint.pprint(cspr.node.show_leader_logs())
                leaderlogs = []# cspr.node.show_leader_logs()
                for llog in cspr.node.show_leader_logs():
                    _llog = {
                        "created_at_time": date_crop(llog["created_at_time"]),
                        "scheduled_at_time": date_crop(llog["scheduled_at_time"]),
                        "scheduled_at_date": llog["scheduled_at_date"],
                        "finished_at_time": date_crop(llog["finished_at_time"]),
                    }
                    if "wake_at_time" in llog:
                        _llog["wake_at_time"] = date_crop(llog["wake_at_time"])

                    _llog["status"] = self.determine_status(llog)
                    leaderlogs.append(_llog)
                if leaderlogs is not None and len(leaderlogs) > 0:
                    header = leaderlogs[0].keys()
                    rows =  [x.values() for x in leaderlogs]
                    table = tabulate(rows, header, tablefmt="psql")
                    print(table)
                else:
                    print("Leader logs are empty")

            if choice == '17': #  Show Chain Settings.
                self.clear()
                pprint.pprint(cspr.node.show_settings())

            if choice == "18": #  janalyze.py aggreate blocks
                self.clear()
                analyze.aggregate()

            if choice == "19": #  janalyze.py distribution
                self.clear()
                analyze.distribution()

            if choice == '20': #  Genesis Decode.
                self.clear()
                print(cspr.cli.genesis_decode())

            if choice == '21': #  Fork Check
                self.clear()
                analyze.forkcheck()

            if choice == 'f': #  Show Config.
                self.clear()
                pprint.pprint(settings)

            if choice == 'v': #  Show Versions.
                self.clear()
                cspr.versions()

            if choice == 'q':  # Quit.
                self.end_loop = True

            if choice == 'c':  # Clear.
                self.clear()

            if choice == "u":
                self.clear()
                print(cspr.db.user)

            if choice == "s":
                self.clear()
                pprint.pprint(settings)

            if choice == "i":
                self.clear()
                filepath = input("PATH TO accounts.yaml: ")
                if os.path.isfile(filepath):
                    try:
                        toimport = parse_yaml(filepath, file=True)
                    except:
                        print("PARSING ERROR")
                    for iacc in toimport:
                        self.save_acct_by_secret(iacc["secret"])
                else:
                    print("FILE NOT FOUND")
            if choice == "e":
                self.clear()
                accts = cspr.db.all_acct()
                _accts = []
                for acct in accts:
                    _accts.append({
                        "address": acct[1],
                        "public": acct[3],
                        "secret": acct[2]
                    })
                _type = input("EXPORT FORMAT? (json[j] / yaml[y]): ")
                if _type.lower() in ("yaml", "y"):
                    yaml.save_file(_accts, location=f"config/accounts.yaml")
                elif _type.lower() in ("json", "j"):
                    with open('config/accounts.json', 'w') as f:
                        json.dump(_accts, f, indent=4)
                else:
                    print("Invalid format selected")

if __name__ == "__main__":
    if sys.platform == 'win32':
        print("Windows not supported")
        sys.exit(2)
    cliui = CliInterface()
    cliui.clear()
    cliui.run()
