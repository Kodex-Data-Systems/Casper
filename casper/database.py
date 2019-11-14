import sys, sqlite3, getpass, os
import os.path
from .utils import mk_timestamp, hash256, verify_password
ABSOLUTEPATH = os.path.abspath(os.path.dirname(__file__))
# os.environ["PYTHONIOENCODING"] = "utf-8"

class Database(object):
    def __init__(self, settings, USER_PWD, module="Fernet"):
        if "savefragments" in settings:
            self.savefragments = True
        else:
            self.savefragments = False
        self.cipher = None
        self.cryptomodule = module
        self.cryptomodules = ["Fernet", "PyCrypto"]
        if module not in self.cryptomodules:
            print("NO CRYPTO MODULE")
            self.cryptomodule = None
            #sys.exit(2)

        if "dbpath" not in settings:
            sys.exit(2)
            if os.path.isfile(settings["dbpath"]) is not True:
                sys.exit(2)

        self.filepath = settings["dbpath"]
        self.connection = sqlite3.connect(self.filepath)
        self.cursor = self.connection.cursor()
        self._check_tables()
        self._load_cipher(USER_PWD, module)

    def _load_sql(self, file):
        with open (os.path.join(ABSOLUTEPATH, "sql/" + file), "r") as file:
            data = file.read().replace('\n', '')
            return data

    def _load_cipher(self, USER_PWD,module=None):
        if module is None:
            self.cipher = None
            return None
        if module == "Fernet":
            from .fernet import FernetCipher
            self.cipher = FernetCipher(USER_PWD)
        if module == "PyCrypto":
            from .aes import AESCipher
            self.cipher = AESCipher(USER_PWD)

#  TOOLS AND HELPERS
    def _check_tables(self):
        self.cursor.execute(self._load_sql("create_account_table.sql"))
        self.cursor.execute(self._load_sql("create_user_table.sql"))
        self.cursor.execute(self._load_sql("create_poolcerts_table.sql"))
        self.cursor.execute(self._load_sql("create_fragment_table.sql"))
        return

    def _decrypt_rows(self, rows):
        out = []
        for row in rows:
            _acct_id = row[0]
            _acct_addr = row[1]
            _acct_secret = self.cipher.decrypt(row[2])
            _acct_public = self.cipher.decrypt(row[3])
            _out = [_acct_id, _acct_addr, _acct_secret, _acct_public, row[4]]
            # print(f'ENCRYPTED ROW OUTPUT\n{row}')
            out.append(_out)

        return out


#  USER QUERIES ######################
    def _create_user(self, hashedpwd, name):
        self.cursor.execute(
            self._load_sql("insert_user.sql"),
            (hashedpwd, name,  mk_timestamp())
        )
        self.connection.commit()
        return

    def _get_users(self, user=None):
        if user is None:
            return self.cursor.execute("SELECT * FROM user").fetchall()
        else:
            return self.cursor.execute("SELECT * FROM user WHERE name=?", (user,)).fetchall()

    def _verify_user(self, userpwd=None, user=None):

        if userpwd is None:
            userpwd = input("PLEASE ENTER YOUR PASSWORD\n")
        hashedpwd = hash256(userpwd)
        _user_row = self._get_users(user)

        #  checking if usertable is not empty!
        if len(_user_row) <= 0:
            print("NO USER IN DB")
            _new_name = input("ENTER NEW USERNAME\n")
            _new_pwd = getpass.getpass("ENTER NEW PASSWORD (min 8 chars incl number + specialchars):\n")
            #  here we should verify password-strength!
            if verify_password(_new_pwd) is False:
                print("PASSWORD TO WEAK")
                sys.exit(2)
            _new_pwd = hash256(_new_pwd)
            self._create_user(_new_pwd,  _new_name)
            return self._verify_user(userpwd)

        #  comparing passwords
        _stored_hash = _user_row[0][1]
        if _stored_hash != hashedpwd:
            print("WRONG PASSWORD")
            sys.exit(2)
        else:
            self.user = _user_row[0]
            self._load_cipher(userpwd, self.cryptomodule)
            print("USER LOGGED IN")
            return True

#  ACCOUNT QUERIES
    def all_acct(self):
        encrypted_rows = self.cursor.execute(
            "SELECT * FROM accounts WHERE user_id=?",
            (int(self.user[0]),)
        ).fetchall()

        if len(encrypted_rows) > 0:
            if self.cipher is None:
                return encrypted_rows
            return self._decrypt_rows(encrypted_rows)
        else:
            return None

    def get_acct_by_id(self, _id):
        try:
            encrypted_rows = self.cursor.execute(
                "SELECT * FROM accounts WHERE id=?",
                (_id, )
            ).fetchall()

            if len(encrypted_rows) <= 0:
                print(f"ACCOUNT WITH id: {_id} NOT FOUND!")
                return False

            #  decrypting rows
            if self.cipher is None:
                _acct_row = encrypted_rows
            else:
                _acct_row = self._decrypt_rows(encrypted_rows)

            return _acct_row[0]
        except:
            return None

    def save_acct(self, _sk, _pk, _acct):
        #  check if account already in db
        if self._acct_exists(_pk) is True:
            print(f"ACCOUNT {_acct} ALREADY IN DB")
            return

        #  Verify if valid keyset?
        #  encrypting data
        _crypt_module = "RAW"
        if self.cipher is not None:
            _sk = self.cipher.encrypt(_sk)
            _pk = self.cipher.encrypt(_pk)
            _crypt_module = self.cryptomodule

        self.cursor.execute(self._load_sql("insert_account.sql"),
            (_acct, _sk,_pk, _crypt_module, mk_timestamp(), int(self.user[0]))
        )
        self.connection.commit()
        return

    def save_fragment(self, account, fragment_id, value):
        if self.savefragments is False:
            return
        self.cursor.execute(self._load_sql("insert_fragment.sql"),
            (account, fragment_id, value, mk_timestamp())
        )
        print(f"FRAGMENT {fragment_id} SAVED TO DB")
        self.connection.commit()
        return

    def _acct_exists(self, secret):
        allaccounts = self.all_acct()
        if allaccounts is not None:
            for row in allaccounts:
                if secret in row:
                    return True
        return False
