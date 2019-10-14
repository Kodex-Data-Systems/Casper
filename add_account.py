import sqlite3


class AddAccount:
    def __init__(self):
        self.added = False
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (list INTEGER,
        account VARCHAR(64), secret VARCHAR(64), public VARCHAR(64))""")

    def get_index(self):
        self.index = self.cursor.execute("""SELECT * FROM accounts ORDER BY
        list DESC LIMIT 1""")
        list_index = ([key[0] for key in self.index])
        try:
            self.index = list_index[0] + 1
        except IndexError:
            self.index = 1

    def get_keys(self):
        self.get_index()
        self.sk = input('Enter secret key: ')
        self.pk = input('Enter public key: ')
        self.acct = input('Enter account key: ')

        self.cursor.execute("""INSERT INTO accounts (list, account, secret,
        public) VALUES (?, ?, ?, ?)""", 
            (self.index, self.acct, self.sk, self.pk))
        self.connection.commit()
        self.connection.close()
        return True        