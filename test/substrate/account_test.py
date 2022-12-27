"""Account testing"""

import logging

from .utils import start_local_connection, ALICE_ADDRESS, ACTIVATION_URL, DOCUMENT_LINK, ALICE_IDENTITY, DOCUMENT_HASH
from substrate import account

substrate = start_local_connection()
test_account = account.Account(substrate, ALICE_IDENTITY)


def test_activate_account():
    """test activate account"""
    try:
        account.Account.activate(ALICE_ADDRESS, ACTIVATION_URL)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_accept_terms_and_conditions():
    """test accept terms and conditions"""
    try:
        test_account.accept_terms_and_conditions(DOCUMENT_LINK, DOCUMENT_HASH)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_signed_terms_and_conditions():
    """test signed terms and conditions"""
    signed_terms_and_conditions = account.Account.signed_terms_and_conditions(substrate, ALICE_ADDRESS)

    if signed_terms_and_conditions.value is not None and len(signed_terms_and_conditions) > 0:
        assert True
    else:
        assert False


def test_get_account_by_identity():
    """test get account with an identity"""

    try:
        test_account.get()
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_is_validator_by_identity():
    """test is validator with an identity"""

    assert not test_account.is_validator()


def test_get_account_by_public_key():
    """test get account with a public key"""

    try:
        account.Account.get_from_public_key(substrate, ALICE_ADDRESS)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_get_balance_by_public_key():
    """test get account with a public key"""

    try:
        account.Balance.get_balance_from_public_key(substrate, ALICE_ADDRESS)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False
