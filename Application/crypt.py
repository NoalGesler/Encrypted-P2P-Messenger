from Crypto.Cipher import DES3
from Crypto.Util import Counter
from Crypto import Random
import hashlib

"""
code referenced from: https://gist.github.com/xuecan/7230348
"""

# GLOBAL VARIABLES
# iv = Random.new().read(DES3.block_size)


def _make_des3_encryptor(key, iv):
    encryptor = DES3.new(key, DES3.MODE_CBC, iv)
    return encryptor


def des3_encrypt(key, iv, data):
    print("Key: ", key)
    print("Data: ", data)

    m = hashlib.md5()
    m.update(key.encode('utf8'))
    key = m.digest()

    print("")
    print("M: ", str(m))
    print("Key: ", str(key))
    print("IV: ", str(iv))
    print("")

    encryptor = _make_des3_encryptor(key, iv)
    pad_len = 8 - len(data) % 8  # length of padding
    padding = chr(pad_len) * pad_len  # PKCS5 padding content
    data += padding
    data = data.encode('utf8')
    return encryptor.encrypt(data)


def des3_decrypt(key, iv, data):
    m = hashlib.md5()
    m.update(key.encode('utf8'))
    key = m.digest()
    print("")
    print("M: ", str(m))
    print("Key: ", str(key))
    print("IV: ", str(iv))
    print("")

    encryptor = _make_des3_encryptor(key, iv)
    result = encryptor.decrypt(data)

    pad_len = result[-1]
    result = result[:-pad_len]
    return result
