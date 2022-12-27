"""utils module to be used in testing"""

import os
from substrateinterface import SubstrateInterface

from substrate.identity import Identity

ACTIVATION_URL = "https://activation.dev.grid.tf/activation/activate"
# TODO change to ALICE ones
ALICE_MNEMONICS = "trophy asthma barrel bachelor shell unknown helmet cram favorite wrist tissue visa"
ALICE_ADDRESS = "5HB3uy5fQDXtcEu2yhKMNwoSgVKLnKGtmp7zniPtrotyNm8u"
ALICE_IDENTITY = Identity.generate_from_phrase(ALICE_MNEMONICS)

IP = "201:1061:b395:a8e3:5a0:f481:1102:e85a"
DOCUMENT_LINK = "http://zos.tf/terms/v0.1"
DOCUMENT_HASH = "9021d4dee05a661e2cb6838152c67f25"
TEST_NAME = "test_name"

GIGABYTE = 1024 * 1024 * 1024


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
