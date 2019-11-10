import sys, subprocess, time, pprint, json
from tabulate import tabulate

from casper import CasperCore
from casper.utils import verify_password

_USER_PWD = input("Enter your Password: ")

_MENU = """
Please choose an option:

(1) Create New Testnet Address   (2) Import Existing Address  (3) Load Address
(4) Create Stake Pool            (5) Delegate Stake           (6) Send Transaction
(7) Display Current Address      (8) Check Balance            (9) Show All Accounts

(10) Show Message Log            (11) Show Node stats         (12) Show Established Peers
(13) Show Stake Pools            (14) Show Stake              (15) Show Blockchain Size
(16) Show Leader Logs            (17) Show Settings

(v) Show Versions                (i) View User Info           (f) View Config File
(e) Export All Accounts          (c) Clear Screen             (q) Quit
"""

with open('config/settings.json', 'r') as json_file:
    settings = json.load(json_file)
    if "cryptomodule" in settings:
        _DEFAULT_CRYPTO = settings["cryptomodule"]
    else:
        _DEFAULT_CRYPTO = input("ENTER CRYPT MODULE (Fernet, PyCrypto, RAW): ")
        if _DEFAULT_CRYPTO is "RAW":
            _DEFAULT_CRYPTO = None

casper = CasperCore(settings, USER_PWD=_USER_PWD, CRYPTO_MOD=_DEFAULT_CRYPTO)

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

    def clear(self):
        cls_platforms = ["linux", "linux2", "darwin"]
        if sys.platform == 'win32':
            subprocess.call('cls', shell=True)
        elif sys.platform in cls_platforms:
            subprocess.call('clear', shell=True)
        else:
            self.typed_text('Command not compatible with your OS', 0.002)

    def run(self):
        while not self.end_loop:
            print(_MENU)
            choice = input('Your Choice: ')

            if choice == '1':  # Create.
                self.clear()
                _sk, _pk, _ak = casper.cli.create_acct()
                casper.db.save_acct(_sk, _pk, _ak)
                self.typed_text(f'Account Created: {_ak}', 0.002)

            if choice == '2':  # Import existing.
                self.clear()
                _sk = input("Input Secret Key: ")
                _pk = input("Input Public Key: ")
                _ak = input("Input Account Address: ")
                casper.db.save_acct(_sk, _pk, _ak)

                self.typed_text(f'Account Added: {_ak}', 0.002)
                print('\n\n')
                self.clear()

            if choice == '3':  # Load.
                self.clear()
                myaccounts = casper.db.all_acct()
                if myaccounts is not None:
                    for acct in myaccounts:
                        print(acct[0], acct[1])

                    _id = input("\nSelect Acount Number: ")
                    try:
                        _selected = casper.db.get_acct_by_id(int(_id))
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
                    casper.cli.create_pool(public, secret, account, pool_name)

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
                    casper.cli.create_delegation_certificate(pool, public, secret, account)

                else:
                    print("You Need To Load An Account First")

            if choice == '6':  # Send Tx.
                self.clear()
                if self.account is not None:
                    sender = self.account[1]
                    secret = self.account[2]
                    amount = int(input('Enter Send Amount: '))
                    receiver = input('Receiver: ')
                    rounds = input("Send Single Transaction (Y/n): ").lower()
                    if rounds == "y":
                        self.clear()
                        casper.cli.send_single_tx(
                            amount,
                            sender,
                            receiver,
                            secret
                        )
                    else:
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

                else:
                    print("You Need To Load An Account First")

            if choice == '7':  # Display current.
                self.clear()
                if self.account is None:
                    print("No Account Loaded")
                else:
                    print(f'Loaded Account: {self.account}')

            if choice == '8':  # Check balance.
                self.clear()
                if self.account is None:
                    print("No Account Loaded")
                else:
                    self.clear()
                    try:
                        addr, balance, nonce = casper.cli.show_balance(self.account[1], raw=False)
                        print(f"Address: {addr}\nBalance: {balance}\nNonce: {nonce}")
                        get_pool = (casper.cli.show_balance(self.account[1], raw=True)).split(':')
                        print(f'Pool: {get_pool[3].strip()[4:-8]}')

                    except:
                        print("0")

            if choice == "9": # Show all accounts
                self.clear()
                pprint.pprint(casper.db.all_acct())

            if choice == '10': # Message log.
                self.clear()
                pprint.pprint(casper.cli.message_logs())

            if choice == '11': # Node stats.
                self.clear()
                pprint.pprint(casper.node.show_node_stats())

            if choice == '12': #  Show Peers.
                self.clear()
                pprint.pprint(casper.node.show_peers())

            if choice == '13': #  Show Stake Pools.
                self.clear()
                pools = (casper.node.show_stake_pools())
                pprint.pprint(pools)
                pool_len = str(len(pools))
                print()
                self.typed_text(f'Number of registered pools: {pool_len}', 0.004)

            if choice == '14': #  Show Stake.
                self.clear()
                stake = pprint.pprint(casper.node.show_stake())
                print(tabulate(stake))

            if choice == '15': #  Show Chain Size.
                self.clear()
                pprint.pprint(casper.cli.show_blockchain_size())

            if choice == '16': #  Show Leaders Logs.
                self.clear()
                pprint.pprint(casper.node.show_leader_logs())

            if choice == '17': #  Show Chain Settings.
                self.clear()
                pprint.pprint(casper.node.show_settings())

            if choice == 'f': #  Show Versions.
                self.clear()
                pprint.pprint(settings)

            if choice == 'i': #  Show Versions.
                self.clear()
                print("USER INFO\n")

            if choice == 'v': #  Show Versions.
                self.clear()
                casper.versions()

            if choice == 'q':  # Quit.
                self.end_loop = True

            if choice == 'c':  # Clear.
                self.clear()

            if choice == "u":
                self.clear()
                print(casper.db.user)

            if choice == "s":
                self.clear()
                pprint.pprint(settings)

            if choice == "e":
                self.clear()
                with open('config/export.json', 'w') as f:
                    json.dump(casper.db.all_acct(), f)
                print("ALL ACCOUNTS EXPORTED")


if __name__ == "__main__":

    if sys.platform == 'win32':
                print("Windows not supported 🦄")
                sys.exit(2)
    cliui = CliInterface()
    cliui.clear()
    print (9 * " 👻 ")
    cliui.run()
