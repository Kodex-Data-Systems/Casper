import subprocess

from config import NODE

class MessageLog:
    def __init__(self):
        try:
            log = subprocess.check_output('jcli rest v0 message logs -h ' + NODE + '/api', shell=True).decode()
            print(log)
        except subprocess.CalledProcessError:
            print('Unable to connect')