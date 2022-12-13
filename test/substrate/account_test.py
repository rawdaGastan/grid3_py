"""Account testing"""

import logging

from test.substrate.utils import start_local_connection
from substrate.account import get_account_info_from_public_key, get_balance_from_public_key

def test_get_account():
    """test get account with a public key"""

    substrate = start_local_connection()
    address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"

    info = get_account_info_from_public_key(address, substrate)
    assert info.nonce == 790

def test_get_balance():
    """test get account with a public key"""

    substrate = start_local_connection()
    address = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY"


    try:
        get_balance_from_public_key(address, substrate)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False