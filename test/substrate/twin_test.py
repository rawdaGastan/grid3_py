"""Twin testing"""

import logging

from .utils import start_local_connection, ALICE_MNEMONICS, ALICE_ADDRESS
from substrate import identity, twin


def test_get_twin_by_public_key():
    """test get twin ID with a public key"""

    substrate = start_local_connection()

    try:
        twin.get_twin_by_public_key(ALICE_ADDRESS, substrate)
        assert True
    except Exception as exp:
        logging.exception(exp)
        assert False

def test_get_twin_by_id():
    """test get twin with ID"""
        
    substrate = start_local_connection()
    test_twin = twin.get_twin_by_id(146, substrate)
    
    assert test_twin.id == 146
    
def test_get_twin():
    """test get twin with ID"""

    substrate = start_local_connection()
    test_identity = identity.new_identity_from_sr25519_mnemonics(ALICE_MNEMONICS)
        
    test_twin = twin.get_twin_by_id(146, substrate)
    
    assert test_twin.id == 146
    