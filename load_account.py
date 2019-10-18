import sqlite3


class AccountLoader:
    def __init__(self):
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()
        self.db_list = []
        self.sk_list = []
        self.index_list = []
        self.is_account = True

    def view_account(self):
        try:
            #  Create a list of accountkeys, secret keys and indexes.
            db_row = self.cursor.execute("""SELECT * FROM accounts""")
            db_acct_key = [self.db_list.append((row[0], row[1])) for row in db_row]
            db_row = self.cursor.execute("""SELECT * FROM accounts""")
            db_sk = [self.sk_list.append((row[0], row[2])) for row in db_row]
            db_row = self.cursor.execute("""SELECT * FROM accounts""")
            db_index = [self.index_list.append(row[0]) for row in db_row]
            print()
            print('Index    Account key')
            db_printout = [print(index, '      ', key)
                           for index, key in self.db_list]
            self.connection.close()

        except sqlite3.OperationalError:
            print('No accounts found\n')

    def load_account(self, index):
        for i in self.db_list:
            if i[0] == index and index in self.index_list:
                return (i[1], True) #  Return account key and True indicating account loaded
        return ('', False) #  Return empty string and False indicating account not loaded

    def load_sk(self, index):
        #  Return secret key based on index for use in send_tx
        for i in self.sk_list:
            if i[0] == index:
                return i[1]                