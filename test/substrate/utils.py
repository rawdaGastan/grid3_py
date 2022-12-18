"""utils module to be used in testing"""

import os
from substrateinterface import SubstrateInterface
import ipaddress

from substrate import identity

ACTIVATION_URL = "https://activation.dev.grid.tf/activation/activate"

ALICE_MNEMONICS = "trophy asthma barrel bachelor shell unknown helmet cram favorite wrist tissue visa"
ALICE_ADDRESS = "5HB3uy5fQDXtcEu2yhKMNwoSgVKLnKGtmp7zniPtrotyNm8u"
ALICE_IDENTITY = identity.new_identity_from_sr25519_mnemonics(ALICE_MNEMONICS)

IP = str(ipaddress.IPv6Address("201:1061:b395:a8e3:5a0:f481:1102:e85a"))
DOCUMENT_LINK = "someDocument"


def start_local_connection():
    """start a substrate local connection to test"""
    try:
        if "CI" in os.environ:
            sub = SubstrateInterface(url="ws://127.0.0.1:9944")
        else:
            sub = SubstrateInterface(url="wss://tfchain.dev.grid.tf")
        assert True
        return sub

    except ValueError:
        assert False
