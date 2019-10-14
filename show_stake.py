import subprocess

from config import NODE


class NodeStats:
    def __init__(self):
        try:
            print()
            stake = subprocess.check_output('jcli rest v0 stake get -h ' + NODE + '/api', shell=True).decode()
            print(stake)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
