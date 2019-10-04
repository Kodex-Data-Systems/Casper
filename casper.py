import sys
import os
import time

import create_account as ca


def typed_text(string, sleep_time):
    ''' Mimic human typing '''
    for letter in string:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(sleep_time)


def run_function():
    print('Please choose an option:\n')
    print('1) Create new testnet account')
    print()
    choice = input('Your Choice: ')
    if choice == '1':
        bot = ca.AccountCreator()
        keys = bot.create_account()
        bot.db_commit(keys)


if __name__ == "__main__":
    typed_text('CASPER v0.1 -- Kodex Data Systems 2019', 0.05)
    print()

    run_function()
