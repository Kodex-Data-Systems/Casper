import base64, os
from .utils import hash256
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

os.environ["PYTHONIOENCODING"] = "utf-8"

class FernetCipher(object):
    def __init__(self, pwd, salt=None):
        self.hash256 = hash256
        self.password = str.encode(pwd)
        if salt is None:
            self.salt = b'+Eh\x98k\\\x1eR\xcf\xf8\nn\x86\xca\xd6\xc8'
        else:
            self.salt = str.encode(salt)

        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(
            self.kdf.derive(self.password)
        )
        self.f = Fernet(self.key)

    def encrypt(self, message):
        _msg = str.encode(message)
        token = self.f.encrypt(_msg)
        token = token.decode("ascii")
        return token

    def decrypt(self, token):
        token = str.encode(token)
        return self.f.decrypt(token).decode('ascii')
