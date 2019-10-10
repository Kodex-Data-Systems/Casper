import os


class BalanceViewer:
    def __init__(self, account_key, node):
        self.account_key = account_key
        self.node = node
        os.system('jcli rest v0 account get ' + self.account_key +
                  ' -h ' + self.node + '/api > balance.json')
        with open('balance.json', 'r') as f:
            print(f.read())
        os.remove('balance.json')
        

