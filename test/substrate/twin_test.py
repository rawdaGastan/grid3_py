"""Twin testing"""

import logging

from .utils import start_local_connection, ALICE_IDENTITY, ALICE_ADDRESS, IP
from substrate import twin

substrate = start_local_connection()
test_twin = twin.Twin(substrate, ALICE_IDENTITY)
test_twin_id = 0


def test_create_twin():
    """test create twin"""
    global test_twin_id
    test_twin_id = test_twin.create(IP)
    assert test_twin_id != 0


def test_update_twin():
    """test update twin"""
    try:
        test_twin.update(IP)
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
    twin_id = twin.Twin.get_twin_id_from_public_key(substrate, ALICE_ADDRESS)
    assert twin_id == test_twin_id


def test_get_twin_by_id():
    """test get twin with ID"""
    twin_info = twin.Twin.get_from_id(substrate, test_twin_id)
    assert twin_info.id == test_twin_id
