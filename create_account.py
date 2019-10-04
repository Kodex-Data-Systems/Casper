import os
import sys
import time
import sqlite3


class AccountCreator:
    def __init__(self):
        self.connection = sqlite3.connect('account.db')
        self.c = self.connection.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS accounts (account VARCHAR(64), secret VARCHAR(64),
        public VARCHAR(64))""")

    def create_account(self):
        ''' Create private, public and address key '''
        os.system('jcli key generate --type ed25519 > s.sk')
        with open('s.sk', 'r') as f:
            self.secret = f.read()[:-1]
        os.remove('s.sk')

        os.system('echo ' + self.secret + ' | jcli key to-public > p.pk')
        with open('p.pk', 'r') as f:
            self.public = f.read()[:-1]
        os.remove('p.pk')

        os.system('jcli address account ' + self.public + ' --testing > a.ac')
        with open('a.ac', 'r') as f:
            self.account = f.read()[:-1]
        os.remove('a.ac')

        return self.secret, self.public, self.account

    def db_commit(self, *args):
        self.sk, self.pk, self.acct = args[0]

        self.c.execute("""INSERT INTO accounts (account, secret, public) VALUES (?, ?, ?)""",
                       (self.acct, self.sk, self.pk))
        self.connection.commit()
        print('Account Created')
