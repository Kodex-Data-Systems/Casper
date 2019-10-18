import sqlite3


class AddAccount:
    def __init__(self):
        self.added = False
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (list VARCHAR(64),
        account VARCHAR(64), secret VARCHAR(64), public VARCHAR(64),
        current_count INTEGER, incremented_count INTEGER, new_count INTEGER)""")

    def get_index(self):
        #  Select last entry from DB.
        self.index = self.cursor.execute("""SELECT * FROM accounts ORDER BY
        list DESC LIMIT 1""")
        #  Retrieve index number.
        list_index = ([key[0] for key in self.index])

        try:
            #  Add next in order.
            self.index = str(int(list_index[0]) + 1)
        except IndexError:
            #  If no entries in DB, create entry 1.
            self.index = '1'

    def get_keys(self):
        self.get_index()
        self.sk = input('Enter secret key: ')
        self.pk = input('Enter public key: ')
        self.acct = input('Enter account address: ')

        self.cursor.execute("""INSERT INTO accounts (list, account, secret,
        public, current_count, incremented_count, new_count) VALUES (?, ?, ?, ?, ?, ?, ?)""", 
            (self.index, self.acct, self.sk, self.pk, 0, 0, 0))
        self.connection.commit()
        self.connection.close()
        return True        