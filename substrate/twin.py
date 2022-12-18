"""Twin module"""
import hashlib
from substrateinterface import SubstrateInterface
from .identity import Identity
import ipaddress


class Twin_Info:
    """Twin info class"""

    def __init__(self, version: int, id: int, account_id: bytes, ip: ipaddress.IPv4Address, entities: list):
        self.version = version
        self.id = id
        self.account_id = account_id
        self.ip = ip
        self.entities = entities


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
        twin_id = get_twin_by_public_key(self.identity.public_key, self.substrate)
        if twin_id != None:
            return get_twin_by_id(twin_id, self.substrate)

    def create(self, ip: str):
        """creates a new twin for account ID

        Args:
            ip (str): the ip for the twin

        Raises:
            Exception: creating a new twin failed
        """
        call = self.substrate.compose_call("TfgridModule", "create_twin", {"ip": ip})

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        result = self.substrate.submit_extrinsic(extrinsic, True, True)

        if not result.is_success or result.error_message != None:
            raise Exception("creating a new twin failed with error: ", result.error_message)

    def update(self, ip: str):
        """updates a twin with the ip

        Args:
            ip (str): the updated ip for the twin

        Raises:
            Exception: updating a new twin failed
        """
        call = self.substrate.compose_call("TfgridModule", "update_twin", {"ip": ip})

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        result = self.substrate.submit_extrinsic(extrinsic, True, True)

        if not result.is_success or result.error_message != None:
            raise Exception("updating a new twin failed with error: ", result.error_message)

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


def get_twin_by_id(id: int, substrate: SubstrateInterface):
    """get the twin info using ID

    Args:
        id (int): the twin id
        substrate (SubstrateInterface): substrate instance

    Raises:
        Exception: twin not found

    Returns:
        Twin_Info: the info for a twin
    """
    twin = substrate.query("TfgridModule", "Twins", [id])
    if twin["id"].value == 0:
        raise Exception("twin not found")

    version = twin["version"].value
    twin_id = twin["id"].value
    account_id = twin["account_id"].value
    ip = twin["ip"].value
    entities = twin["entities"].value

    return Twin_Info(version, twin_id, account_id, ip, entities)


def get_twin_by_public_key(public_key: bytes, substrate: SubstrateInterface):
    """get twin ID from a public key

    Args:
        public_key (bytes): identity public key
        substrate (SubstrateInterface): substrate client
    """

    twin_id = substrate.query("TfgridModule", "TwinIdByAccountID", [public_key])
    if twin_id == 0:
        raise Exception("twin not found")

    return twin_id


def signed_terms_and_conditions(public_key: bytes, substrate: SubstrateInterface):
    """get the signed terms and conditions

    Args:
        public_key (bytes): identity public key
        substrate (SubstrateInterface): substrate client
    """

    terms_and_conditions = substrate.query("TfgridModule", "UsersTermsAndConditions", [public_key])
    return terms_and_conditions
