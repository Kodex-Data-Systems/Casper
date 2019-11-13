import base64, hashlib, os
from Crypto import Random
from Crypto.Cipher import AES
from .utils import hash256
os.environ["PYTHONIOENCODING"]

class AESCipher():
    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()
        self.hash256 = hash256

    def encrypt(self, raw):
        _raw = self._pad(raw)
        _iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, _iv)
        return base64.b64encode(_iv + cipher.encrypt(_raw)).decode("utf8")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
