import subprocess

from config import STORAGE


class ShowBlockchainSize:
    def __init__(self):
        try:
            print()
            size = subprocess.check_output('ls -h ' + STORAGE, shell=True).decode()
            print(size)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
