import os

from expungeservice.crypto import CredentialsCipher


class TestEncryption():

    def test_it_encrypts_and_decrypts(self):

        secret_key = os.urandom(32)

        cipher = CredentialsCipher(secret_key)

        secrets = {"to_happiness": "money",
                   "number": 4}

        encrypted = cipher.encrypt(secrets)

        assert type(encrypted) == bytes

        decrypted = cipher.decrypt(encrypted)

        assert decrypted["to_happiness"] == secrets["to_happiness"]
