import sqlite3


class AccountLoader:
    def __init__(self):
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()
        self.db_list = []
    def view_account(self):
        db_row = self.cursor.execute("""SELECT * FROM accounts""")
        db_index = [self.db_list.append((row[0], row[1])) for row in db_row]
        print() 
        print('Index    Account key')
        db_printout = [print(index,'      ', key) for index, key in self.db_list]
        self.connection.close()
        
    def load_account(self, index):
        for i in self.db_list:
            if i[0] == int(index):
                return i[1]
        