"""Account module"""
from dataclasses import dataclass
import hashlib
import http
import requests

from substrateinterface import SubstrateInterface

from substrate.exceptions import AcceptingTermsAndConditionsFailed, AccountActivationFailed
from .identity import Identity


@dataclass
class Balance:
    """Account balance class"""

    free: int
    reserved: int
    misc_frozen: int
    fee_frozen: int

    @staticmethod
    def get_balance_from_public_key(substrate: SubstrateInterface, public_key: bytes):
        """get balance info of the provided public key

        Args:
            public_key (bytes): given public key
            substrate (SubstrateInterface): substrate instance

        Returns:
            Balance: account balance
        """

        account_info = substrate.query("System", "Account", [public_key])
        data = account_info["data"]

        free = data["free"].value
        reserved = data["reserved"].value
        misc_frozen = data["misc_frozen"].value
        fee_frozen = data["fee_frozen"].value

        return Balance(free, reserved, misc_frozen, fee_frozen)


@dataclass
class AccountInfo:
    """Account info class"""

    nonce: int
    consumers: int
    providers: int
    sufficients: int
    balance: Balance


class Account:
    """Account class"""

    def __init__(self, substrate: SubstrateInterface, identity: Identity):
        self.substrate = substrate
        self.identity = identity
        self.account_info = None

    def get(self):
        """get account of the provided account ID"""
        account_info = self.substrate.query("System", "Account", [self.identity.public_key])

        nonce = account_info["nonce"].value
        consumers = account_info["consumers"].value
        providers = account_info["providers"].value
        sufficients = account_info["sufficients"].value

        data = account_info["data"]

        free = data["free"].value
        reserved = data["reserved"].value
        misc_frozen = data["misc_frozen"].value
        fee_frozen = data["fee_frozen"].value

        balance = Balance(free, reserved, misc_frozen, fee_frozen)

        self.account_info = AccountInfo(nonce, consumers, providers, sufficients, balance)

        return self.account_info

    def accept_terms_and_conditions(self, document_link: str, document_hash: str):
        """accepting terms and conditions

        Args:
            document_link (str): document link
            document_hash (str): document hash

        Raises:
            AcceptingTermsAndConditionsFailed: accepting terms and conditions failed with error
        """

        signed_terms = self.signed_terms_and_conditions(self.substrate, self.identity.public_key)
        if signed_terms.value is None and len(signed_terms) > 0:
            return

        call = self.substrate.compose_call(
            "TfgridModule",
            "user_accept_tc",
            {"document_link": document_link, "document_hash": document_hash},
        )

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        call_response = self.substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success:
            raise AcceptingTermsAndConditionsFailed(call_response.error_message)

    def is_validator(self):
        """check if the account ID is a validator"""

        validators = self.substrate.query("TFTBridgeModule", "Validators")
        return self.identity.address in validators

    @staticmethod
    def get_from_public_key(substrate: SubstrateInterface, public_key: bytes):
        """get account info of the provided public key

        Args:
            public_key (bytes): given public key
            substrate (SubstrateInterface): substrate instance

        Returns:
            AccountInfo: account information including balance, nonce, ..
        """

        account_info = substrate.query("System", "Account", [public_key])

        nonce = account_info["nonce"].value
        consumers = account_info["consumers"].value
        providers = account_info["providers"].value
        sufficients = account_info["sufficients"].value

        data = account_info["data"]

        free = data["free"].value
        reserved = data["reserved"].value
        misc_frozen = data["misc_frozen"].value
        fee_frozen = data["fee_frozen"].value

        balance = Balance(free, reserved, misc_frozen, fee_frozen)

        return AccountInfo(nonce, consumers, providers, sufficients, balance)

    @staticmethod
    def signed_terms_and_conditions(substrate: SubstrateInterface, public_key: bytes):
        """get the signed terms and conditions

        Args:
            public_key (bytes): identity public key
            substrate (SubstrateInterface): substrate client
        """

        terms_and_conditions = substrate.query("TfgridModule", "UsersTermsAndConditions", [public_key])
        return terms_and_conditions

    @staticmethod
    def activate(address: str, activation_url: str):
        """activate account for funding

        Args:
            address (str): identity address
            substrate (SubstrateInterface): substrate client
        """
        response: requests.Response = requests.post(activation_url, {"substrateAccountID": address})

        if response.status_code != http.HTTPStatus.OK and response.status_code != http.HTTPStatus.CONFLICT:
            raise AccountActivationFailed("account activation failed")
