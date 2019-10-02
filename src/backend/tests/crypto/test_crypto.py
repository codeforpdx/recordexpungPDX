import os
import unittest

from expungeservice.crypto import DataCipher


class TestEncryption(unittest.TestCase):

    def setUp(self):

        secret_key = os.urandom(32)
        self.cipher = DataCipher(secret_key)

    def test_it_encrypts_and_decrypts(self):

        secret = {"to_happiness": "money"}

        encrypted = self.cipher.encrypt(secret)

        assert type(encrypted) == bytes

        decrypted = self.cipher.decrypt(encrypted)

        assert decrypted["to_happiness"] == secret["to_happiness"]

    def test_other_data_types(self):

        a = [1, 2, 3, 4, 5, 6]

        assert a == self.cipher.decrypt(self.cipher.encrypt(a))

        b = 123456.78

        assert b == self.cipher.decrypt(self.cipher.encrypt(b))

        c = "a secret message"

        assert c == self.cipher.decrypt(self.cipher.encrypt(c))
