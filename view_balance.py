import subprocess
from casper import Interface


class BalanceViewer(Interface):
    def __init__(self, account_key, node):
        try:
            self.account_key = account_key
            self.node = node
            output = subprocess.check_output('jcli rest v0 account get ' + self.account_key +
                                            ' -h ' + self.node + '/api', shell=True).decode()
            Interface.typed_text(output, 0.01)
            print('\n\n')
            
        except subprocess.CalledProcessError:
            Interface.typed_text('Unable to view balance, account has not yet received a tx or node is offline.', 0.02)
            print('\n\n') 