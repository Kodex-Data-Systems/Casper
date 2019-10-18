import subprocess


class ShowJcliVersion:
    def __init__(self):
        try:
            print()
            version = subprocess.check_output('jcli --full-version', shell=True).decode()
            print(version)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
