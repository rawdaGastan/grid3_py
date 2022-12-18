"""contract testing"""

'''
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
'''
