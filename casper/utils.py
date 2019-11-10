import base64, hashlib, calendar
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re

def verify_password(password):
    RegexLength=re.compile(r'^\S{8,}$')
    RegexDigit=re.compile(r'\d')
    RegexLower=re.compile(r'[a-z]')
    if RegexLength.search(password) == None or RegexDigit.search(password) == None or RegexLower.search(password) == None: # or RegexUpper.search(password) == None :
        return False
    else:
        return True

def hash256(string):
    return hashlib.sha256(string.encode()).hexdigest()

def mk_timestamp():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    return unixtime

def to_base32(input):
    return base64.b32encode(bytearray(str(input), 'ascii')).decode('utf-8')

def to_hex(input):
    return input.encode("utf-8").hex()
