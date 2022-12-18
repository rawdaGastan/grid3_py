"""utils module to be used in testing"""

import os
from substrateinterface import SubstrateInterface

ALICE_MNEMONICS = "bottom drive obey lake curtain smoke basket hold race lonely fit walk"
ALICE_ADDRESS = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"


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
