"""Twin module"""
from dataclasses import dataclass
from substrateinterface import SubstrateInterface

from substrate.exceptions import TwinCreationException, TwinUpdateException
from .identity import Identity
import ipaddress


@dataclass
class TwinInfo:
    """Twin info class"""

    version: int
    id: int
    account_id: str
    ip: str
    entities: list


class Twin:
    """Twin class"""

    def __init__(self, substrate: SubstrateInterface, identity: Identity):
        self.substrate = substrate
        self.identity = identity
        self.twin_info = None

    def get(self):
        """get the twin info for the account ID

        Returns:
            Twin_Info: the info for a twin
        """
        twin_id = self.get_twin_id_from_public_key(self.substrate, self.identity.public_key)
        if twin_id == None:
            raise ValueError("account with public key: " + self.identity.public_key + "has no twin")

        return self.get_from_id(self.substrate, twin_id)

    def create(self, ip: str):
        """creates a new twin for account ID

        Args:
            ip (str): the ip for the twin

        Raises:
            Exception: creating a new twin failed
        """
        try:
            ipaddress.IPv6Address(ip)
        except ValueError:
            raise ValueError

        twin = self.get()
        if twin != None:
            return twin.id

        call = self.substrate.compose_call("TfgridModule", "create_twin", {"ip": ip})

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        result = self.substrate.submit_extrinsic(extrinsic, True, True)

        if not result.is_success or result.error_message != None:
            raise TwinCreationException(result.error_message)

        twin_id = self.get().id
        return twin_id

    def update(self, ip: str):
        """updates a twin with the ip

        Args:
            ip (str): the updated ip for the twin

        Raises:
            Exception: updating a new twin failed
        """
        try:
            ipaddress.IPv6Address(ip)
        except ValueError:
            raise ValueError

        call = self.substrate.compose_call("TfgridModule", "update_twin", {"ip": ip})

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        result = self.substrate.submit_extrinsic(extrinsic, True, True)

        if not result.is_success or result.error_message != None:
            raise TwinUpdateException(result.error_message)

    @staticmethod
    def get_from_id(substrate: SubstrateInterface, id: int):
        """get the twin info using ID

        Args:
            id (int): the twin id
            substrate (SubstrateInterface): substrate instance

        Raises:
            Exception: not found

        Returns:
            Twin_Info: the info for a twin
        """
        twin = substrate.query("TfgridModule", "Twins", [id])
        if twin == None:
            raise ValueError(f"twin with id {id} is not found")

        version = twin["version"].value
        twin_id = twin["id"].value
        account_id = twin["account_id"].value
        ip = twin["ip"].value
        entities = twin["entities"].value

        return TwinInfo(version, twin_id, account_id, ip, entities)

    @staticmethod
    def get_twin_id_from_public_key(substrate: SubstrateInterface, public_key: bytes):
        """get twin ID from a public key

        Args:
            public_key (bytes): identity public key
            substrate (SubstrateInterface): substrate client
        """

        twin_id = substrate.query("TfgridModule", "TwinIdByAccountID", [public_key])
        if twin_id == 0:
            raise ValueError(f"twin with public key {public_key} is not found")

        return twin_id
