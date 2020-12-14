from passlib.hash import sha256_crypt
from os import urandom
from typing import Tuple
import base64


def encrypt_base64(password: str) -> Tuple[str,str]:
    salt = str(urandom(32))
    concat = password + salt
    _hash = sha256_crypt.encrypt(concat)

    _hash_b64 = base64.b64encode(_hash.encode('utf-8'))
    salt_b64 = base64.b64encode(salt.encode('utf-8'))

    return _hash_b64,salt_b64


def verifyHash_base64(password: str,_hash_base64: str,salt_base64: str) -> bool:
    _hash = base64.b64decode(_hash_base64)
    salt = base64.b64decode(salt_base64)

    _hash = _hash.decode('utf-8')
    salt = salt.decode('utf-8')
    
    concat = password + salt

    return sha256_crypt.verify(concat,_hash)


