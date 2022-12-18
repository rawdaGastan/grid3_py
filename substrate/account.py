"""Account module"""
import hashlib
import http
from urllib import request
import requests

from substrateinterface import SubstrateInterface
from .identity import Identity


class Balance:
    """Account balance class"""

    def __init__(self, free=0, reserved=0, misc_frozen=0, fee_frozen=0):
        self.free = free
        self.reserved = reserved
        self.misc_frozen = misc_frozen
        self.fee_frozen = fee_frozen


class AccountInfo:
    """Account info class"""

    def __init__(self, nonce, consumers, providers, sufficients, balance: Balance):
        self.nonce = nonce
        self.consumers = consumers
        self.providers = providers
        self.sufficients = sufficients
        self.balance = balance


class Account:
    """Account class"""

    def __init__(self, substrate: SubstrateInterface, identity: Identity):
        self.substrate = substrate
        self.identity = identity
        self.account_info = None

    def get_account(self):
        """get account of the provided account ID"""
        account_info = self.substrate.query("System", "Account", [self.identity.public_key])

        nonce = account_info["nonce"].value
        consumers = account_info["consumers"].value
        providers = account_info["providers"].value
        sufficients = account_info["sufficients"].value

        data: map = account_info["data"]

        free = data["free"].value
        reserved = data["reserved"].value
        misc_frozen = data["misc_frozen"].value
        fee_frozen = data["fee_frozen"].value

        balance = Balance(free, reserved, misc_frozen, fee_frozen)

        self.account_info = AccountInfo(nonce, consumers, providers, sufficients, balance)

        return self.account_info

    def accept_terms_and_conditions(self, document_link: str):
        """accepting terms and conditions

        Args:
            document_link (str): document link

        Raises:
            Exception: accepting terms and conditions failed with error
        """

        signed_terms = signed_terms_and_conditions(self.identity.public_key, self.substrate)
        if signed_terms != None and len(signed_terms) > 0:
            return

        document_hash = hashlib.md5(document_link.encode()).hexdigest()

        call = self.substrate.compose_call(
            "TfgridModule",
            "user_accept_tc",
            {"document_link": document_link, "document_hash": document_hash},
        )

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        result = self.substrate.submit_extrinsic(extrinsic, True, True)

        if not result.is_success or result.error_message != None:
            raise Exception("accepting terms and conditions failed with error: ", result.error_message)

    def is_validator(self):
        """check if the account ID is a validator"""

        validators = self.substrate.query("TFTBridgeModule", "Validators")
        print(validators)

        for validator in validators:
            if self.identity == validator:
                return True

        return False


def activate_account(address: str, activation_url: str):
    """activate account for funding

    Args:
        address (str): identity address
        substrate (SubstrateInterface): substrate client
    """
    response: requests.Response = requests.post(activation_url, {"substrateAccountID": address})

    if response.status_code != http.HTTPStatus.OK and response.status_code != http.HTTPStatus.CONFLICT:
        raise Exception("account activation failed")


def signed_terms_and_conditions(public_key: bytes, substrate: SubstrateInterface):
    """get the signed terms and conditions

    Args:
        public_key (bytes): identity public key
        substrate (SubstrateInterface): substrate client
    """

    terms_and_conditions = substrate.query("TfgridModule", "UsersTermsAndConditions", [public_key])
    return terms_and_conditions


def get_account_info_from_public_key(public_key: bytes, substrate: SubstrateInterface):
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

    data: map = account_info["data"]

    free = data["free"].value
    reserved = data["reserved"].value
    misc_frozen = data["misc_frozen"].value
    fee_frozen = data["fee_frozen"].value

    balance = Balance(free, reserved, misc_frozen, fee_frozen)

    return AccountInfo(nonce, consumers, providers, sufficients, balance)


def get_balance_from_public_key(public_key: bytes, substrate: SubstrateInterface):
    """get balance info of the provided public key

    Args:
        public_key (bytes): given public key
        substrate (SubstrateInterface): substrate instance

    Returns:
        Balance: account balance
    """

    account_info = substrate.query("System", "Account", [public_key])
    data: map = account_info["data"]

    free = data["free"].value
    reserved = data["reserved"].value
    misc_frozen = data["misc_frozen"].value
    fee_frozen = data["fee_frozen"].value

    return Balance(free, reserved, misc_frozen, fee_frozen)
