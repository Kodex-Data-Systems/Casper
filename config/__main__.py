import sys, platform, getpass
sys.path.append(".")

import json, json, pprint, sys, sqlite3, os
from casper.utils import hash256, mk_timestamp, verify_password

ABSOLUTEPATH = os.path.abspath(os.path.dirname(__file__))

with open('package.json', 'r') as json_file:
    package = json.load(json_file)

_SCREEN = """
Welcome to Casper Setup.

You can press Enter at any prompt to use the following default settings, or enter your own.

        REST API SERVER:  http://localhost:3101
        Database Storage Path:  ./accounts.db
        Genesis Hash:  bad49dbbd149ee6cbe1f172d4a727b5e3cf9ea057651f303758eff9cb6ce8387
        Crypto Module:  Fernet is default, PyCrypto is the alternative.
        Blockchain Storage Path:  /tmp/storage


"""
class CasperSetup(object):
    def __init__(self):
        self.usersettings = {}
        self.start()


    def start(self):
        print(_SCREEN)
        _default_node = "http://localhost:3101"
        self.usersettings["version"] = package["version"]
        self.usersettings["node"] = _default_node
        _user_node = input("Input REST API Server Address: ")
        _user_db = input("Input Database Storage Path: ")
        _user_genesis = input("Input Genesis Hash: ")
        _user_crypto = input("Input Crypto Module: ")
        _user_jmpath = input("Input Blockchain Storage Path: ")

        self.usersettings["platform"] = platform.platform()
        if "http" in _user_node:
            self.usersettings["node"] = _user_node

        if ".db" in _user_db:
            self.usersettings["dbpath"] = _user_db
        else:
            self.usersettings["dbpath"] = "config/accounts.db"

        if _user_genesis != "":
            self.usersettings["genesis"] = _user_genesis
        else:
            self.usersettings["genesis"] = "0c6db1bc6b4794c8d3913529ebe6ba986684c3b23bfe4879fde37dabbc71ba93"

        if _user_crypto != "":
            self.usersettings["cryptomodule"] = _user_crypto
        else:
            self.usersettings["cryptomodule"] = "Fernet"

        if _user_jmpath != "":
            self.usersettings["jmpath"] = _user_jmpath
        else:
            self.usersettings["jmpath"] = "/tmp/jormungandr"

        _create_new_db = input("Create New Database? (y/n): ")

        if "y" in _create_new_db:
            self._create_db()

        self._save_user_settings()

    def _save_user_settings(self):
        pprint.pprint(self.usersettings)
        with open('config/settings.json', 'w') as fp:
            json.dump(self.usersettings, fp, indent=4)

    def _load_sql(self, _file):
        cp = os.path.dirname(__file__)
        if cp == ".":
            _path = os.path.join(os.path.dirname(__file__), "casper/sql/" + _file)
        elif cp == "./config":
            _path = os.path.join(os.path.dirname(__file__), "../casper/sql/" + _file)

        with open (_path, "r") as file:
            data = file.read().replace('\n', '')
            return data

    def _create_db(self):
        connection = sqlite3.connect(self.usersettings["dbpath"])
        cursor = connection.cursor()
        cursor.execute(self._load_sql("create_account_table.sql"))
        cursor.execute(self._load_sql("create_user_table.sql"))
        cursor.execute(self._load_sql("create_poolcerts_table.sql"))

        _new_name = input("Enter New Username: ")
        _new_pwd = getpass.getpass("Enter New Password (min 8 chars incl number + specialchars): ")

        if verify_password(_new_pwd) is False:
            print("PASSWORD TO WEAK")
            sys.exit(2)

        _new_pwd = hash256(_new_pwd)

        cursor.execute(
            self._load_sql("insert_user.sql"),
            (_new_pwd, _new_name,  mk_timestamp())
        )
        connection.commit()

if __name__ == "__main__":
    SETUP = CasperSetup()
