import sys
import os
import time

from config import NODE
import load_account as load
import create_account as ca
import view_balance as vb


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
        Interface.typed_text('CASPER v0.3 -- Kodex Data Systems 2019', 0.05)
        print('\n\n')

    def run_function(self):
        while not self.end_loop:
            print('Please choose an option:')
            print('1) View accounts')
            print('2) Load account')
            print('3) Display current account')
            print('4) Check balance')
            print('5) Create new testnet account')
            print('6) Exit')
            choice = input('Your Choice: ')

            if choice == '1':
                print()
                try:
                    user_account = load.AccountLoader()
                    user_account.view_account()
                except Exception as e:
                    print('Database does not exist')
                print()
                #self.account_loaded = True
                # self.account = load_account.loaded_account
                # Interface.typed_text('Account loaded', 0.05)
                # print('\n\n')

            if choice == '2':
                user_account = load.AccountLoader()
                user_account.view_account()
                print()
                Interface.typed_text('Select the index number of the account you would like to load:', 0.03)
                print()
                index = input('Index number: ')
                print()
                self.account = user_account.load_account(index)
                self.account_loaded = True


            if choice == '3':
                if self.account_loaded:
                    try:
                        Interface.typed_text('Account: ' + self.account, 0.01)
                        print('\n\n')
                    except TypeError:
                        Interface.typed_text('Error, please try reloading', 0.05)
                        print('\n\n')
                else:
                    Interface.typed_text('No account loaded', 0.05)
                    print('\n\n')

            if choice == '4':
                if self.account_loaded:
                    vb.BalanceViewer(self.account, NODE)
                else:
                    Interface.typed_text('No account loaded', 0.05)
                    print('\n\n')

            if choice == '5':
                create = ca.AccountCreator()
                keys = create.create_account()
                create.db_commit(keys)
                if create.created == True:
                    Interface.typed_text('Account Created', 0.05)
                    print('\n\n')

            if choice == '6':
                self.end_loop = True


if __name__ == "__main__":
    bot = Interface()

    bot.run_function()
