import subprocess
import os

from config import NODE


class SendTx:
    def __init__(self, amount, sender, receiver, sk):
        self.NODE = NODE
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.sk = sk
        self.tx_sent = False

    def node_values(self):
        #  Extract the tx fee (coefficient and constant) from the node using string slicing.
        data = subprocess.check_output('jcli rest v0 settings get -h ' + self.NODE + '/api', shell=True).decode().replace(' ', '')
        data_dict = dict(s.split(':') for s in (data.split('\n')[7:9]))
        self.coefficient = data_dict['coefficient']
        self.constant = data_dict['constant']

        return (self.coefficient, self.constant)

    def get_counter(self):
        try:
            #  Extract the required counter.
            os.system('jcli rest v0 account get ' + self.sender +
                    ' -h ' + self.NODE + '/api > balance.tmp')
            with open('balance.tmp', 'r') as f:
                counter = f.read().split()[2]
            os.remove('balance.tmp')
        
            return int(counter)

        except IndexError:
            print('Unable to connect to node, verify node is online.')
        
    def send_tx(self, counter):
        try:
            node_values = self.node_values()

            #  Required transaction fees.
            coefficient, constant = int(node_values[0]), int(node_values[1])
            total_fees = str(int(self.amount) + (coefficient * 2) + constant)

            #  Begin tx procedure through JCLI.
            os.system('jcli transaction new --staging file.staging')
            os.system('jcli transaction add-account ' + self.sender + ' ' + total_fees + ' --staging file.staging')
            os.system('jcli transaction add-output ' + self.receiver + ' ' + self.amount + ' --staging file.staging')
            os.system('jcli transaction finalize --staging file.staging')
            witness = subprocess.check_output('jcli transaction id --staging file.staging', shell=True).decode()[:-1]

            #  Create files for witness via python. JCLI requires environmental variables.
            with open('witness.output.tmp', 'w+') as f:
                pass
            with open('witness.secret.tmp', 'w+') as f:
                f.write(self.sk)

            #  Include genesis block.
            os.system('jcli transaction make-witness ' + witness + 
            ' --genesis-block-hash adbdd5ede31637f6c9bad5c271eec0bc3d0cb9efb86a5b913bb55cba549d0770 --type "account" --account-spending-counter ' +
            str(counter) + ' witness.output.tmp witness.secret.tmp')
            
            #  Add witness.
            os.system('jcli transaction add-witness witness.output.tmp --staging file.staging')
            info = subprocess.check_output('jcli transaction info --fee-constant ' + str(constant) + ' --fee-coefficient ' +
            str(coefficient) + ' --staging file.staging', shell=True).decode()

            #  Display transaction info for sender to verify.
            print(info)
            print()

            #  Sender to confirm transaction.
            cont = input('Commit transaction to blockchain? (y/n): ')
            
            if cont == 'y':
                #  Sender confirms, tx sends, return tx sent.
                os.system('jcli transaction seal --staging file.staging')
                os.system('jcli transaction to-message --staging file.staging | jcli rest v0 message post -h ' + self.NODE + '/api')
                #  Remove temp files
                os.remove('witness.output.tmp')
                os.remove('witness.secret.tmp')
                os.remove('file.staging')
                return True
            else:
                #  Remove temp files, return tx not sent.
                os.remove('witness.output.tmp')
                os.remove('witness.secret.tmp')
                os.remove('file.staging')
                return False

        except IndexError:
            print('Unable to connect to node')
            print('Verify account is active and check node')
            return False

        except ValueError:
            print('Unable to send, verify amount is an integer')
            return False