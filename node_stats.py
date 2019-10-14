import subprocess

from config import NODE


class NodeStats:
    def __init__(self):
        try:
            print()
            stats = subprocess.check_output('jcli rest v0 node stats get -h ' + NODE + '/api', shell=True).decode()
            print(stats)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
