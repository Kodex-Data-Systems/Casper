import os
import sqlite3
import subprocess


class AccountCreator:
    def __init__(self):
        self.created = False
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (list INTEGER, account VARCHAR(64), secret VARCHAR(64),
        public VARCHAR(64))""")

    def create_account(self):
        ''' Create private, public and address key '''
        self.secret = subprocess.check_output('jcli key generate --type ed25519extended', shell=True).decode()[:-1]
        
        os.system('echo ' + self.secret + ' | jcli key to-public > p.pk')
        with open('p.pk', 'r') as f:
            self.public = f.read()[:-1]
        os.remove('p.pk')

        self.account = subprocess.check_output('jcli address account ' + self.public + ' --testing', shell=True).decode()[:-1]

        return self.secret, self.public, self.account

    def db_commit(self, keys):
        self.sk, self.pk, self.acct = keys

        index = self.cursor.execute(
            """SELECT * FROM accounts ORDER BY list DESC LIMIT 1""")
        list_index = ([key[0] for key in index])
        try:
            index = list_index[0] + 1
        except IndexError:
            index = 1

        self.cursor.execute("""INSERT INTO accounts (list, account, secret, public) VALUES (?, ?, ?, ?)""",
                            (index, self.acct, self.sk, self.pk))
        self.connection.commit()
        self.connection.close()
        self.created = True
