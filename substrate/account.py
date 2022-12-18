"""Account module"""
import base58

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

    def is_validator(self):
        """check if the account ID is a validator"""

        validators = self.substrate.query("TFTBridgeModule", "Validators")
        print(validators)

        for validator in validators:
            if self.identity == validator:
                return True

        return False


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
