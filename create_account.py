import os
import sqlite3
import subprocess


class AccountCreator:
    def __init__(self):
        self.created = False
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (list VARCHAR(64), account VARCHAR(64),
        secret VARCHAR(64), public VARCHAR(64), current_count INTEGER,
        incremented_count INTEGER, new_count INTEGER)""")

    def create_account(self):
        ''' Create private, public and address key '''

        #  Generate secret using JCLI.
        self.secret = subprocess.check_output('jcli key generate --type ed25519extended', shell=True).decode()[:-1]
        
        #  echo system call can not generate required result, save result to file instead.
        os.system('echo ' + self.secret + ' | jcli key to-public > p.tmp')
        with open('p.tmp', 'r') as f:
            self.public = f.read()[:-1]
        os.remove('p.tmp')

        #  Generate account using JCLI.
        self.account = subprocess.check_output('jcli address account ' + self.public + ' --testing', shell=True).decode()[:-1]

        return self.secret, self.public, self.account

    def db_commit(self, keys):
        self.sk, self.pk, self.acct = keys

        index = self.cursor.execute(
            """SELECT * FROM accounts ORDER BY list DESC LIMIT 1""")
        list_index = ([key[0] for key in index])
        try:
            #  Get the index number of the next row to insert new account.
            index = str(int(list_index[0]) + 1)
        except IndexError:
            #  If database does not exist, create DB with account at index 1.
            index = '1'

        self.cursor.execute("""INSERT INTO accounts (list, account, secret, public,
        current_count, incremented_count, new_count) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            (str(index), self.acct, self.sk, self.pk, 0, 0, 0))
        self.connection.commit()
        self.connection.close()
        self.created = True
