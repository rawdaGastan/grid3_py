"""bridge testing"""

import logging
import pytest
from substrate.bridge import MintTransaction, RefundTransaction
from substrate.exceptions import (
    ProposeOrVoteMintTransactionException,
    RefundTransactionCreationOrAddingSigException,
    SetRefundTransactionExecutedException,
)
from test.substrate.utils import ALICE_ADDRESS, start_local_connection, ALICE_IDENTITY


substrate = start_local_connection()


def test_refund_transactions():
    """test refund transactions"""

    try:
        RefundTransaction.create_refund_transaction_or_add_sig(substrate, ALICE_IDENTITY, "test_hash", "", 1, "", "", 0)
    except RefundTransactionCreationOrAddingSigException as exp:
        logging.exception(exp)

    # ValidatorNotExists
    with pytest.raises(SetRefundTransactionExecutedException) as e:
        RefundTransaction.set_refund_transaction_executed(substrate, ALICE_IDENTITY, "test_hash")

    assert RefundTransaction.is_refunded_already(substrate, "test_hash") == False

    refund_transaction = RefundTransaction.get(substrate, "test_hash")

    assert refund_transaction.tx_hash == ""


def test_mint_transactions():
    """test mint transactions"""

    # ValidatorNotExists
    with pytest.raises(ProposeOrVoteMintTransactionException) as e:
        MintTransaction.propose_or_vote_mint_transaction(substrate, ALICE_IDENTITY, "test_id", ALICE_ADDRESS, 1)

    assert MintTransaction.is_minted_already(substrate, "test_id") == False
