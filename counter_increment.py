import sqlite3
import time

class CountChecker:
    def __init__(self, counter, index):
        ''' Increment check will be used to allow multiple transactions. 
        Transactions must be sent with the node counter nonce in ascending order.
        
        Within the cli a transaction must be confirmed before the next can be sent. 
        Once the transaction is confirmed the counter nonce will increment by +1.

        Using CountChecker the user can send as many transactions as desired while the 
        class handles the counter increments accordingly. '''

        self.is_incrementing = False
        self.counter = counter
        self.index = index
        self.connection = sqlite3.connect('account.db')
        self.cursor = self.connection.cursor()

    def return_count(self):
        counter_update = ("""UPDATE accounts SET current_count= ? WHERE list = ?""")
        counter_data = (self.counter, self.index)
        self.cursor.execute(counter_update, counter_data)
        self.connection.commit()
        
        #  Call 3 values based on index number.
        select_index = (""" SELECT current_count, incremented_count, new_count
        FROM accounts WHERE list = ? """)
        index_values = self.cursor.execute(select_index, self.index)
        self.connection.commit()

        for i in index_values:
            self.current_count = i[0]
            self.incremented_count = i[1]
            self.new_count = i[2]

        if self.current_count == self.new_count:
            self.increment_counter = 0
        elif self.new_count < self.current_count:
            self.new_count = self.current_count

        self.incremented_count = self.new_count - self.current_count
        self.new_count = self.current_count + self.incremented_count
        self.send_count = self.new_count

        return self.new_count
        
    def increment_update(self):
        counter_update = ("""UPDATE accounts SET 
        current_count = ?, incremented_count= ?, new_count = ? WHERE list = ?""")
        counter_data = (self.current_count, self.incremented_count,
            self.new_count, self.index)

        self.cursor.execute(counter_update, counter_data)
        self.connection.commit()

        print()
        print('Current count: ', self.current_count)
        print('Send count:', self.send_count)
        print('Incremented count:', self.incremented_count)
        print('New count: ', self.new_count)

    def reset_counter(self):
        counter_update = ("""UPDATE accounts SET 
        current_count = ?, incremented_count= ?, new_count = ? WHERE list = ?""")
        counter_data = (self.counter, 0, 0, self.index)

        self.cursor.execute(counter_update, counter_data)
        self.connection.commit()    

    def view_count(self):
        counter_view = (""" SELECT current_count, incremented_count, new_count
        FROM accounts WHERE list = ? """)
        counter_data = self.index
        view_data = self.cursor.execute(counter_view, counter_data)
        self.connection.commit() 

        for data in view_data:
            current_count = data[0]
            incremented_count = data[1]
            new_count = data[2]

        print()
        print('Current count:', current_count)
        print('Incremented count:', incremented_count)
        print('New count', new_count)
        print()
        time.sleep(3)

# bot = CountChecker(0, '1')
# bot.view_count()
