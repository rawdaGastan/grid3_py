"""Identity module"""

from substrateinterface import Keypair, KeypairType

NETWORK = 42


class Identity:
    """Identity is a user identity"""

    def __init__(self, key_pair: Keypair, sign, identity_type: int, address: str, public_key: bytes, uri):
        self.key_pair = key_pair
        self.sign = sign
        self.identity_type = identity_type
        self.address = address
        self.public_key = public_key
        self.uri = uri


def generate_identity_from_key_pair(key_pair: Keypair):
    """generates an identity from a given key pair

    Args:
        key_pair (Keypair): substrate key pair

    Returns:
        Identity: user identity
    """
    identity = Identity(
        key_pair=key_pair,
        sign=key_pair.sign,
        identity_type=key_pair.crypto_type,
        address=key_pair.ss58_address,
        public_key=key_pair.public_key,
        uri=key_pair.derive_path,
    )

    return identity


def new_identity_from_ed25519_key(private_key: bytes):
    """creates a new identity from an ed25519 private key

    Args:
        private_key (bytes): ed25519 private key

    Returns:
        Identity: user identity
    """
    crypto_type = KeypairType.ED25519
    key_pair = Keypair.create_from_private_key(private_key, ss58_format=NETWORK, crypto_type=crypto_type)
    return generate_identity_from_key_pair(key_pair)


def new_identity_from_sr25519_phrase(phrase: str):
    """creates a new identity from a phrase

    Args:
        phrase (str): given phrase to generate a key pair

    Returns:
        Identity: user identity
    """
    key_pair = Keypair.create_from_uri(phrase)
    return generate_identity_from_key_pair(key_pair)


def new_identity_from_sr25519_mnemonics(mnemonics: str):
    """creates a new identity from a phrase

    Args:
        mnemonics (str): given mnemonics to generate a key pair

    Returns:
        Identity: user identity
    """
    key_pair = Keypair.create_from_mnemonic(mnemonics)
    return generate_identity_from_key_pair(key_pair)
