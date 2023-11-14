from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



def encrypt_aes(data, password):
    # 使用 PBKDF2 進行密鑰派生
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'salt',
        iterations=100000,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password)

    # 使用 AES 加密
    cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()

    return ciphertext


def decrypt_aes(ciphertext, password):
    # 使用 PBKDF2 進行密鑰派生
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'salt',
        iterations=100000,
        length=32,
        backend=default_backend()
    )
    key = kdf.derive(password)

    # 使用 AES 解密
    cipher = Cipher(algorithms.AES(key), modes.CFB8(), backend=default_backend())
    decryptor = cipher.decryptor()
    data = decryptor.update(ciphertext) + decryptor.finalize()

    return data
