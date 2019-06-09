import base64
import bytes

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass


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

    def encrypt(self, message_string, password_string):
        """
        Encrypt a string
        """
        message = message_string.encode(encoding=self.ENCODING)
        return self.get_fernet(password_string).encrypt(message)

        password = password_string.encode(encoding=self.ENCODING)
        message = message_string.encode(encoding=self.ENCODING)
        key = base64.urlsafe_b64encode(self.kdf.derive(password))
        f = Fernet(key)
        token = f.encrypt(message)
        return token.hex()

    def decrypt(self, encrypted, password_string):
        """
        Decrypt a message
        """
        token = bytes.fromhex(encrypted)
        try:
            message = self.get_fernet(
                password_string
            ).decrypt(
                token
            ).decode(
                encoding=self.ENCODING
            )
        except InvalidToken:
            message = None

        return message
