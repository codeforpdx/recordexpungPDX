from cryptography.fernet import Fernet
import json
import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class DataCipher:
    """
    wraps an initialized Fernet cipher object to encrypt and decrypt
    data objects.

    Anything that can be serialized/deserialized with json.dumps and
    json.loads can be encrypted/decrypted.
    """

    def __init__(self, key=None):

        if key is None:
            key = os.urandom(32)

        if isinstance(key, str):
            key_as_bytes = key.encode()
        else:
            key_as_bytes = key

        salt_string = "constant so that session cookies carry across restarts of this app"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_string.encode(),
            iterations=100000,
            backend=default_backend()
        )
        hashed_key = kdf.derive(key_as_bytes)
        key_bytes = base64.encodebytes(hashed_key)
        self.cipher = Fernet(key=key_bytes)

    def encrypt(self, data):
        """
        encrypts a serializable data object into a bytes object.
        """

        utf_encoded_json = json.dumps(data).encode("utf-8")

        return self.cipher.encrypt(bytes(utf_encoded_json))

    def decrypt(self, encrypted):
        """
        decrypts a string or bytes object into a json-deserialized object.
        """

        if type(encrypted) == str:
            encrypted = bytes(encrypted, "utf-8")

        json_str = self.cipher.decrypt(encrypted)
        deserialzed_data = json.loads(json_str)

        return deserialzed_data
