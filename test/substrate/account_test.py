"""Account testing"""

import logging

from .utils import start_local_connection, ALICE_MNEMONICS, ALICE_ADDRESS
from substrate import account
from substrate import identity


def test_get_account_by_identity():
    """test get account with an identity"""

    substrate = start_local_connection()

    test_identity = identity.new_identity_from_sr25519_mnemonics(ALICE_MNEMONICS)
    test_account = account.Account(substrate, test_identity)

    try:
        test_account.get_account()
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_is_validator_by_identity():
    """test is validator with an identity"""

    substrate = start_local_connection()

    test_identity = identity.new_identity_from_sr25519_mnemonics(ALICE_MNEMONICS)
    test_account = account.Account(substrate, test_identity)

    assert not test_account.is_validator()


def test_get_account_by_public_key():
    """test get account with a public key"""

    substrate = start_local_connection()

    try:
        account.get_account_info_from_public_key(ALICE_ADDRESS, substrate)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_get_balance_by_public_key():
    """test get account with a public key"""

    substrate = start_local_connection()

    try:
        account.get_balance_from_public_key(ALICE_ADDRESS, substrate)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False
