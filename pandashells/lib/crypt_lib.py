import base64
import sys

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypt:
    """
    This is a class to enable encryption/decryption of ambition secrets.  The
    code was basically copied from
    https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet
    """
    ENCODING = 'UTF-8'

    @property
    def kdf(self):
        """
        Generates an ecnryption key from your password
        """
        return PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b':h\x8a\xff\xda~}Dx\xa8\x80Q\xf3\x92\x93\x06',
            iterations=100000,
            backend=default_backend()
        )

    def get_fernet(self, password_string):
        password = password_string.encode()
        key = base64.urlsafe_b64encode(self.kdf.derive(password))
        return Fernet(key)

    def encrypt(self, message, password_string):
        """
        Encrypt a string
        """
        if isinstance(message, str):
            message = message.encode(encoding=self.ENCODING)
        return self.get_fernet(password_string).encrypt(message)

    def decrypt(self, encrypted, password_string):
        """
        Decrypt a message
        """
        try:
            out = self.get_fernet(password_string).decrypt(encrypted)
        except InvalidToken:
            print('\n\nBad password\n', file=sys.stderr)
            sys.exit(1)

        return out
