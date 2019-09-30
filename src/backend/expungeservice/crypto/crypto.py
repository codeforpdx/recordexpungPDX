
from flask import current_app
import time
from cryptography.fernet import Fernet
import json
import base64


class CredentialsCipher():
    """
    wraps an initialized Fernet cryptography module object with a symmetric
    key to encrypt and decrypt dictionary data objects
    """

    def __init__(self, key=None):

        if key is None:
            key = current_app.config.get('JWT_SECRET_KEY')

        key_bytes = base64.encodebytes(key)
        self.cipher = Fernet(key=key_bytes)

    def encrypt(self, credentials):
        """
        encrypts a dictionary object into a bytes object.
        """

        json_str = json.dumps(credentials)
        utf_encoded = json_str.encode("utf-8")

        encrypted = self.cipher.encrypt(bytes(utf_encoded))

        return encrypted

    def decrypt(self, encrypted):
        """
        decrypts a string or bytes object into dictionary object.
        """
        if type(encrypted) == str:
            encrypted = bytes(encrypted, "utf-8")

        json_str = self.cipher.decrypt(encrypted)
        credentials = json.loads(json_str)

        return credentials
