import subprocess

from config import NODE


class NodeStats:
    def __init__(self):
        try:
            print()
            peers = subprocess.check_output('netstat -tupan |grep jormungandr |grep ESTABLISHED', shell=True).decode()
            print(peers)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
