import sys
import os
import time

from config import NODE
import load_account as load
import create_account as ca
import view_balance as vb
import send_tx as stx
import message_log
import add_account as ac


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
        Interface.typed_text('CASPER v0.4 -- Kodex Data Systems 2019', 0.05)
        print('\n\n')

    def run_function(self):
        while not self.end_loop:
            print('Please choose an option:')
            print('1) Create new testnet account')
            print('2) Load account')
            print('3) Add existing account')
            print('4) Display current account')
            print('5) Check balance')
            print('6) Send tx')
            print('7) Message log')
            print('8) Node stats # Coming soon')
            print('q) Exit')
            print('c) Clear screen')
            choice = input('Your Choice: ')

            if choice == '1': # Create
                create = ca.AccountCreator()
                keys = create.create_account()
                create.db_commit(keys)
                if create.created == True:
                    Interface.typed_text('Account Created', 0.05)
                    print('\n\n')

            if choice == '2': # Load
                user_account = load.AccountLoader()
                is_account = user_account.view_account()
                if is_account:
                    print()
                    Interface.typed_text(
                        'Select the index number of the account you would like to load:', 0.01)
                    print()
                    index = input('Index number: ')
                    self.account = user_account.load_account(index)
                    self.sk = user_account.load_sk(index)
                    self.account_loaded = True
                    Interface.typed_text('Account loaded', 0.05)
                    print('\n\n')

            if choice == '3': # Add existing
                add_acct = ac.AddAccount()
                add_acct.get_keys()
                if add_acct.added == True:
                    Interface.typed_text('Account added', 0.05)
                    print('\n\n')

            if choice == '4': # Display current
                if self.account_loaded:
                    try:
                        Interface.typed_text('Account: ' + self.account, 0.01)
                        print('\n\n')
                    except TypeError:
                        Interface.typed_text(
                            'Error, please try reloading account', 0.05)
                        print('\n\n')
                else:
                    Interface.typed_text('No account loaded', 0.05)
                    print('\n\n')

            if choice == '5': # Check balance
                if self.account_loaded:
                    vb.BalanceViewer(self.account, NODE)
                else:
                    Interface.typed_text('No account loaded', 0.05)
                    print('\n\n')

            if choice == '6': # Send Tx
                print()
                amount = input('Enter send amount: ')
                receiver = input('Enter receiver address: ')
                print()
                transaction = stx.SendTx(amount, self.account, receiver, self.sk)
                tx_sent = transaction.send_tx()
                if tx_sent:
                    Interface.typed_text('Transaction sent for verification', 0.04)
                    print('\n\n')
                else:
                    Interface.typed_text('Transaction failed to send', 0.04)
                    print('\n\n')

            if choice == '7': # Message log
                message_log.MessageLog()

            if choice == 'q': # Quit
                self.end_loop = True

            if choice == 'c': # Clear
                try:
                    os.system('clear')
                except:
                    Exception
                try:
                    os.system('cls')
                except:
                    Exception


if __name__ == "__main__":
    bot = Interface()

    bot.run_function()