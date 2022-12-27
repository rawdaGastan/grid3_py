"""Identity module"""

from dataclasses import dataclass
from substrateinterface import Keypair, KeypairType

SS58_FORMAT = 42


@dataclass
class Identity:
    """Identity is a user identity"""

    def __init__(self, key_pair: Keypair):
        self.key_pair = key_pair
        self.sign = self.key_pair.sign
        self.identity_type = self.key_pair.crypto_type
        self.address = self.key_pair.ss58_address
        self.public_key = self.key_pair.public_key
        self.uri = self.key_pair.derive_path

    @staticmethod
    def generate_from_ed25519_key(private_key: bytes):
        """creates a new identity from an ed25519 private key

        Args:
            private_key (bytes): ed25519 private key

        Returns:
            Identity: user identity
        """
        crypto_type = KeypairType.ED25519
        key_pair = Keypair.create_from_private_key(private_key, ss58_format=SS58_FORMAT, crypto_type=crypto_type)
        return Identity(key_pair)

    @staticmethod
    def generate_from_sr25519_phrase(phrase: str):
        """creates a new identity from a phrase

        Args:
            phrase (str): given phrase to generate a key pair

        Returns:
            Identity: user identity
        """
        key_pair = Keypair.create_from_uri(phrase)
        return Identity(key_pair)

    @staticmethod
    def generate_from_phrase(phrase: str):
        """creates a new identity from a phrase/mnemonic

        Args:
            phrase (str): given mnemonics/phrase to generate a key pair

        Returns:
            Identity: user identity
        """
        key_pair = Keypair.create_from_mnemonic(phrase)
        return Identity(key_pair)


def generate_key_pair_from_phrase(phrase: str):
    """generate key pair from mnemonic/phrase

    Args:
        phrase (str): mnemonic/phrase of polka account

    Returns:
        Keypair: key pair for the phrase/mnemonic
    """
    return Keypair.create_from_mnemonic(phrase)
