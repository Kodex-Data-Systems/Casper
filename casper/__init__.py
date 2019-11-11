import sys, subprocess, json, platform
from .node import Node
from .database import Database
from .cli import Cli
from .utils import get_exec_sh
with open('package.json', 'r') as json_file:
    package = json.load(json_file)
    version = package["version"]

class CasperCore(object):
    def __init__(self, settings, USER_PWD=None, CRYPTO_MOD="Fernet", USER_NAME=None):
        if sys.platform == 'win32':
            print("Windows not supported 🦄")
            sys.exit(2)

        self.executable = get_exec_sh()
        self.settings = settings

        if "version" in self.settings:
            self.version = self.settings["version"]
        else:
            self.version = version

        if USER_PWD is None:
            USER_PWD = input("Enter your Password\n")


        self.versions()

        self.db = Database(self.settings, USER_PWD, CRYPTO_MOD)
        self.node = Node(self.settings)
        self.cli = Cli(self.settings)


        if USER_NAME is None:
            self.db._verify_user(USER_PWD)
        else:
            self.db._verify_user(USER_NAME)


    def versions(self):
        print("STARTING CASPER CORE v" + self.version)
        print("OS", platform.platform())
        jcli_version = self._run("jcli --full-version")
        jormungandr_version = self._run("jormungandr --full-version")
        python_version = self._run("python3 --version")

        if jormungandr_version is None:
            self.settings["NO_JORMUNGANDR"] = True
            print("ERROR JORMUNGANDR NOT INSTALLED")
            #  sys.exit(2) # JORMUNGANDR is not required

        if jcli_version is None:
            print("ERROR JCLI NOT INSTALLED")
            sys.exit(2)

        if python_version is None:
            print("ERROR PYTHON3 NOT INSTALLED")
            sys.exit(2)

        print(jcli_version)
        print(jormungandr_version)
        print(python_version)

    def _run(self, runstring, errorstring=None):
        try:
            version = subprocess.check_output(
                str(runstring),
                shell=True,
                executable=self.executable
            ).decode()
            return version.replace("\n", "")

        except subprocess.CalledProcessError:
            if errorstring is None:
                print(f'Error running command: {runstring}\n')
            else:
                print(str(errorstring))
