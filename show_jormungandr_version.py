import subprocess


class ShowJormungandrVersion:
    def __init__(self):
        try:
            print()
            version = subprocess.check_output('jormungandr --full-version', shell=True).decode()
            print(version)
            
        except subprocess.CalledProcessError:
            print('Unable to connect\n')
