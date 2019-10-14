import subprocess

from config import NODE


class ShowStakePools:
    def __init__(self):
        try:
            print()
            pools = subprocess.check_output('jcli rest v0 stake-pools get -h ' + NODE + '/api', shell=True).decode()
            print(pools)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
