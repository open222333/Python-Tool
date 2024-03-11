from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64


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

### Base64 ###


def convert_str_to_base64(original_string: str):
    """_summary_

    Args:
        original_string (_type_): _description_
    """
    encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
    return encoded_bytes.decode('utf-8')


def convert_base64_to_str(encoded_string: str):
    """Base64 編碼解碼為字符串

    Args:
        encoded_string (_type_): _description_
    """
    decoded_bytes = base64.b64decode(encoded_string)
    return decoded_bytes.decode('utf-8')
