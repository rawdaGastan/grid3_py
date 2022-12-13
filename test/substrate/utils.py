"""utils to be used in testing"""
import os
from substrateinterface import SubstrateInterface


def start_local_connection():
    """start a substrate local connection to test"""
    try:
        if "CI" in os.environ:
            sub = SubstrateInterface(url="ws://127.0.0.1:9944")
        else:
            sub = SubstrateInterface(url="wss://tfchain.dev.grid.tf")
        assert True
        return sub
    except Exception:
        assert False
