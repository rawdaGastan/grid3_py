"""Twin testing"""

import logging

from .utils import start_local_connection, ALICE_MNEMONICS, ALICE_ADDRESS
from substrate import identity, twin

substrate = start_local_connection()
test_identity = identity.new_identity_from_sr25519_mnemonics(ALICE_MNEMONICS)
test_twin = twin.Twin(substrate, test_identity)

document_link = "someDocument"
ip = ":::"
test_twin_id = 0


def test_accept_terms_and_conditions():
    """test accept terms and conditions"""
    try:
        test_twin.accept_terms_and_conditions(document_link)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_create_twin():
    """test create twin"""
    try:
        test_twin.create(ip)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_update_twin():
    """test update twin"""
    try:
        test_twin.update(ip)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False


def test_get_twin():
    """test get twin"""
    twin_info = test_twin.get()
    assert twin_info.id == test_twin_id


def test_get_twin_by_public_key():
    """test get twin ID with a public key"""

    twin_id = twin.get_twin_by_public_key(ALICE_ADDRESS, substrate)
    assert twin_id == test_twin_id


def test_get_twin_by_id():
    """test get twin with ID"""
    twin_info = twin.get_twin_by_id(test_twin_id, substrate)
    assert twin_info.id == test_twin_id


def test_signed_terms_and_conditions():
    """test signed terms and conditions"""
    signed_terms_and_conditions = twin.signed_terms_and_conditions(ALICE_ADDRESS, substrate)

    if signed_terms_and_conditions != None and len(signed_terms_and_conditions) > 0:
        assert True
    else:
        assert False
