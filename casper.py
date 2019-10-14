import sys
import subprocess
import time

from config import NODE
import load_account as load
import create_account as ca
import view_balance as vb
import send_tx as stx
import message_log as ml
import add_account as ac
import node_stats as ns


class Interface:
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

    def __init__(self):
        self.end_loop = False
        self.account_loaded = False
        self.account = ''
        self.sk = ''
        self.counter_iterated = False
        self.counter_iteration = 0

        Interface.typed_text('CASPER v1.1 -- Kodex Data Systems 2019', 0.02)
        print('\n\n')

    def run_function(self):
        while not self.end_loop:
            print('Please choose an option:')
            print('1) Create new testnet account')
            print('2) Add existing account')
            print('3) Load account')
            print('4) Display current account')
            print()
            print('5) Check balance')
            print('6) Send tx')
            print('7) Message log')
            print('8) Node stats')
            print()
            print('q) Exit')
            print('c) Clear screen')
            choice = input('Your Choice: ')

            if choice == '1':  # Create
                create = ca.AccountCreator()
                keys = create.create_account()
                create.db_commit(keys)
                if create.created:
                    Interface.typed_text('Account Created', 0.03)
                    print('\n\n')

            if choice == '2':  # Add existing
                add_acct = ac.AddAccount()
                account_added = add_acct.get_keys()
                if account_added:
                    Interface.typed_text('Account added', 0.04)
                    print('\n\n')

            if choice == '3':  # Load
                user_account = load.AccountLoader()
                user_account.view_account()
                print()
                Interface.typed_text(
                    'Select the number of the account you would like to load from the list:', 0.01)
                print('\n\n')
                index = input('Index number: ')
                return_loaded = user_account.load_account(index) 
                self.account = return_loaded[0]
                self.sk = user_account.load_sk(index)
                self.account_loaded = return_loaded[1]
                if self.account_loaded:
                    self.counter_iterated = False
                    Interface.typed_text('Account loaded', 0.04)
                    print('\n\n')
                elif not self.account_loaded:
                    self.account = ''
                    Interface.typed_text('Account not in list', 0.04)
                    print('\n\n')                

            if choice == '4':  # Display current
                if self.account_loaded:
                    try:
                        Interface.typed_text('Account: ' + self.account, 0.01)
                        print('\n\n')
                    except TypeError:
                        Interface.typed_text(
                            'Error, please try reloading account', 0.04)
                        print('\n\n')
                else:
                    Interface.typed_text('No account loaded', 0.04)
                    print('\n\n')

            if choice == '5':  # Check balance
                if self.account_loaded:
                    vb.BalanceViewer(self.account, NODE)
                else:
                    Interface.typed_text('No account loaded', 0.04)
                    print('\n\n')

            if choice == '6':  # Send Tx
                if self.account_loaded:
                    print()
                    amount = input('Enter send amount: ')
                    receiver = input('Enter receiver address: ')
                    print()
                    transaction = stx.SendTx(amount, self.account, receiver, self.sk)

                    #  If no tx's have been sent in this shell, actual counter nonce is used.
                    if not self.counter_iterated:
                        self.counter_iteration = 100#transaction.get_counter()

                    #  If tx's have been sent counter nonce is manually iterated
                    #  Counter nonce does not change on node until pending transaction is confirmed.

                    print(f'Counter iteration: {self.counter_iteration}')
                    tx_sent = transaction.send_tx(str(self.counter_iteration))

                    if tx_sent:
                        self.counter_iterated = True
                        if self.counter_iterated:
                            self.counter_iteration += 1
                        Interface.typed_text('Transaction sent', 0.04)
                        print('\n\n')
                    else:
                        Interface.typed_text('Transaction failed to send', 0.04)
                        print('\n\n')
                else:
                    Interface.typed_text('No account loaded', 0.04)
                    print('\n\n')

            if choice == '7':  # Message log
                ml.MessageLog()

            if choice == '8':  # Node stats
                ns.NodeStats()

            if choice == 'q':  # Quit
                self.end_loop = True

            if choice == 'c':  # Clear
                if sys.platform == 'win32':
                    subprocess.call('cls', shell=True)
                elif sys.platform == 'linux' or sys.platform == 'linux2' or sys.platform == 'darwin':
                    subprocess.call('clear', shell=True)
                else:
                    Interface.typed_text('Command not compatible with your OS', 0.04)


if __name__ == "__main__":
    bot = Interface()
    bot.run_function()  