from security import encrypt_base64, verifyHash_base64

_hash,salt = encrypt_base64("żółć")
print(_hash,salt)

result = verifyHash_base64("żółć",_hash,salt)

assert result == True

result = verifyHash_base64("żółc",_hash,salt)

assert result == False