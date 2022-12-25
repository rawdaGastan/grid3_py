"""Bridge module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface
from substrate.exceptions import (
    ProposeOrVoteMintTransactionException,
    RefundTransactionCreationOrAddingSigException,
    SetRefundTransactionExecutedException,
)
from substrate.identity import Identity


@dataclass
class StellarSignature:
    "Stellar signature class"

    signature: bytes
    stellar_address: bytes


@dataclass
class RefundTransaction:
    "Refund Transaction class"

    block: int
    amount: int
    target: str
    tx_hash: str
    signatures: list[StellarSignature]
    sequence_number: int

    @staticmethod
    def create_refund_transaction_or_add_sig(
        substrate: SubstrateInterface,
        identity: Identity,
        tx_hash: str,
        target: str,
        amount: int,
        signature: str,
        stellar_address: str,
        sequence_number: int,
    ):
        """create refund transaction or add signature

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): user identity
            tx_hash (str): transaction hash
            target (str): target address for refund
            amount (int): refund amount
            signature (str): signature
            stellar_address (str): stellar address
            sequence_number (int): sequence number

        Raises:
            RefundTransactionCreationOrAddingSigException: Creation failed
        """
        call = substrate.compose_call(
            "TFTBridgeModule",
            "create_refund_transaction_or_add_sig",
            {
                "tx_hash": tx_hash,
                "target": target,
                "amount": amount,
                "signature": signature,
                "stellar_pub_key": stellar_address,
                "sequence_number": sequence_number,
            },
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise RefundTransactionCreationOrAddingSigException(call_response.error_message)

    @staticmethod
    def set_refund_transaction_executed(substrate: SubstrateInterface, identity: Identity, tx_hash: str):
        """set refund transaction executed

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): user identity
            tx_hash (str): transaction hash

        Raises:
            SetRefundTransactionExecutedException: Setting failed
        """
        call = substrate.compose_call(
            "TFTBridgeModule",
            "set_refund_transaction_executed",
            {"tx_hash": tx_hash},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise SetRefundTransactionExecutedException(call_response.error_message)

    @staticmethod
    def is_refunded_already(substrate: SubstrateInterface, tx_hash: str):
        """check if is refunded

        Args:
            substrate (SubstrateInterface): substrate instance
            tx_hash (str): transaction hash

        Raises:
            ValueError: getting failed
        """
        byte_hash = str.encode(tx_hash)
        if len(byte_hash) <= 32:
            byte_hash_32 = byte_hash + bytearray(32 - len(byte_hash))
        else:
            raise ValueError(f"hash length {len(byte_hash)} is not valid")

        refunded_transaction = substrate.query("TFTBridgeModule", "ExecutedRefundTransactions", [byte_hash_32])
        if refunded_transaction["tx_hash"] == tx_hash:
            return True
        return False

    @staticmethod
    def get(substrate: SubstrateInterface, tx_hash: str):
        """check if is refunded

        Args:
            substrate (SubstrateInterface): substrate instance
            tx_hash (str): transaction hash

        Raises:
            ValueError: getting failed
        """
        byte_hash = str.encode(tx_hash)
        if len(byte_hash) <= 32:
            byte_hash_32 = byte_hash + bytearray(32 - len(byte_hash))
        else:
            raise ValueError(f"hash length {len(byte_hash)} is not valid")

        refunded_transaction = substrate.query("TFTBridgeModule", "RefundTransactions", [byte_hash_32])

        print(refunded_transaction)

        signatures: list[StellarSignature] = []
        for signature in refunded_transaction["signatures"].value:
            signatures.append(
                StellarSignature(
                    signature["signature"],
                    signature["stellar_pub_key"],
                )
            )

        return RefundTransaction(
            block=refunded_transaction["block"].value,
            amount=refunded_transaction["amount"].value,
            target=refunded_transaction["target"].value,
            tx_hash=refunded_transaction["tx_hash"].value,
            signatures=signatures,
            sequence_number=refunded_transaction["sequence_number"].value,
        )


@dataclass
class MintTransaction:
    "Mint Transaction class"

    amount: int
    target: str
    block: int
    votes: int

    @staticmethod
    def propose_or_vote_mint_transaction(
        substrate: SubstrateInterface, identity: Identity, tx_id: str, target: str, amount: int
    ):
        """propose or vote mint transaction

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): user identity
            tx_id (str): transaction ID
            target (str): target address for mint
            amount (int): mint amount

        Raises:
            ProposeOrVoteMintTransactionException: Creation failed
        """
        call = substrate.compose_call(
            "TFTBridgeModule",
            "propose_or_vote_mint_transaction",
            {"transaction": tx_id, "target": target, "amount": amount},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise ProposeOrVoteMintTransactionException(call_response.error_message)

    @staticmethod
    def is_minted_already(substrate: SubstrateInterface, tx_id: str):
        """check if is minted

        Args:
            substrate (SubstrateInterface): substrate instance
            tx_id (str): mint hash ID

        Raises:
            ValueError: getting failed
        """
        refunded_transaction = substrate.query("TFTBridgeModule", "ExecutedMintTransactions", [tx_id])
        if refunded_transaction != None:
            return True
        return False
