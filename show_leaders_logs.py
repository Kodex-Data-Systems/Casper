import subprocess

from config import NODE


class ShowLeadersLogs:
    def __init__(self):
        try:
            print()
            log = subprocess.check_output('jcli rest v0 leaders logs get -h ' + NODE + '/api', shell=True).decode()
            print(log)
            
        except subprocess.CalledProcessError:
            print('Unable to connect')
