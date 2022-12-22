"""Contract module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface
from substrate.exceptions import (
    ContractCancelException,
    NameContractCreationException,
    NodeContractCreationException,
    NodeContractUpdateException,
    RentContractCreationException,
    ContractConsumptionException,
)
from substrate.farm import PublicIP

from substrate.node import NodeFeatures, Resources
from .identity import Identity
from typing import Any


@dataclass
class OptionFeatures:
    """option features class"""

    has_value: bool
    as_value: list[NodeFeatures]


@dataclass
class OptionResources:
    """option resources class"""

    has_value: bool
    as_value: Resources


@dataclass
class DeletedState:
    """Deleted state class"""

    is_canceled_by_user: bool
    is_out_of_funds: bool


@dataclass
class ContractState:
    """contract state class"""

    is_created: bool
    is_deleted: bool
    as_deleted: DeletedState
    is_grace_period: bool
    as_grace_period_block_number: int


@dataclass
class NameContract:
    """Name contract class"""

    name: str


@dataclass
class RentContract:
    """Rent contract class"""

    node_id: int


@dataclass
class NodeContract:
    """Node contract class"""

    node_id: int
    deployment_hash: bytes
    deployment_data: str
    public_ips_count: int
    public_ips: list[PublicIP]


@dataclass
class ContractType:
    """Contract type class"""

    is_node_contract: bool
    node_contract: NodeContract
    is_name_contract: bool
    name_contract: NameContract
    is_rent_contract: bool
    rent_contract: RentContract


@dataclass
class Contract:
    """contract class"""

    version: int
    state: ContractState
    contract_id: int
    twin_id: int
    contract_type: ContractType
    solution_provider_id: int

    @staticmethod
    def create_node_contract(
        substrate: SubstrateInterface,
        identity: Identity,
        node_id: int,
        data: str,
        hash: str,
        public_ips: int,
        solution_provider_id: int = None,
    ):
        """create a new node contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            node_id (int): node ID for the contract
            data (str): contract deployment data
            hash (bytes): contract deployment hash
            solution_provider_id (int, optional): solution provider id

        Raises:
            NodeContractCreationException: creating a node contract failed

        Returns:
            int: contract ID
        """
        
        byte_hash = str.encode(hash)
        if len(byte_hash) <= 32:
            byte_hash_32 = byte_hash + bytearray(32 - len(byte_hash))
        else:
            raise ValueError(f"hash length {len(byte_hash)} is not valid")

        contract_id = Contract.get_contract_id_with_hash_and_node_id(substrate, node_id, byte_hash_32)
        if contract_id != 0:
            return contract_id

        call = substrate.compose_call(
            "SmartContractModule",
            "create_node_contract",
            {
                "node_id": node_id,
                "deployment_data": data,
                "deployment_hash": byte_hash_32,
                "public_ips": public_ips,
                "solution_provider_id": solution_provider_id,
            },
        )
        
        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)
        
        if not call_response.is_success or call_response.error_message != None:
            raise NodeContractCreationException(call_response.error_message)

        return Contract.get_contract_id_with_hash_and_node_id(substrate, node_id, byte_hash_32)

    @staticmethod
    def update_node_contract(substrate: SubstrateInterface, identity: Identity, contract_id: int, data: str, hash: str):
        """update a node contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            contract_id (int): contract ID
            data (str): deployment data for contract
            hash (bytes): deployment hash for contract
        """

        byte_hash = str.encode(hash)
        if len(byte_hash) <= 32:
            byte_hash_32 = byte_hash + bytearray(32 - len(byte_hash))
        else:
            raise ValueError(f"hash length {len(byte_hash)} is not valid")

        call = substrate.compose_call(
            "SmartContractModule",
            "update_node_contract",
            {"contract_id": contract_id, "deployment_data": data, "deployment_hash": byte_hash_32},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise NodeContractUpdateException(call_response.error_message)

    @staticmethod
    def get_node_contracts(substrate: SubstrateInterface, node_id: int):
        """get contracts' IDs using node id

        Args:
            substrate (SubstrateInterface): substrate instance
            node_id (int): node ID

        Raises:
            ValueError: contracts not found

        Returns:
            list[int]: contracts ID
        """

        contracts: list[int] = substrate.query("SmartContractModule", "ActiveNodeContracts", [node_id])
        if len(contracts) == 0:
            raise ValueError("can't get contracts with node id: " + node_id)

        return contracts

    @staticmethod
    def get_contract_id_with_hash_and_node_id(substrate: SubstrateInterface, node_id: int, hash: bytes):
        """get contract id with hash and node id

        Args:
            substrate (SubstrateInterface): substrate instance
            node_id (int): node ID
            hash (bytes): description

        Raises:
            ValueError: contract not found

        Returns:
            int: contract ID
        """
        
        contract_id = substrate.query("SmartContractModule", "ContractIDByNodeIDAndHash", [node_id, hash])
        if contract_id == None:
            raise ValueError("can't get ID for a contract with node id: " + node_id)

        return contract_id

    @staticmethod
    def create_name_contract(substrate: SubstrateInterface, identity: Identity, name: str):
        """create a new name contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            name (int): name for the contract
        """
        contract_id = Contract.get_contract_id_by_name_registration(substrate, name)
        if contract_id != 0:
            return contract_id

        call = substrate.compose_call(
            "SmartContractModule",
            "create_name_contract",
            {"name": name},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise NameContractCreationException(call_response.error_message)

        return Contract.get_contract_id_by_name_registration(substrate, name)

    @staticmethod
    def get_contract_id_by_name_registration(substrate: SubstrateInterface, name: str):
        """get contract ID from name

        Args:
            substrate (SubstrateInterface): substrate instance
            name (str): contract name

        Returns:
            int: contract ID
        """

        return substrate.query("SmartContractModule", "ContractIDByNameRegistration", [name])

    @staticmethod
    def create_rent_contract(
        substrate: SubstrateInterface, identity: Identity, node_id: int, solution_provider_id: int = None
    ):
        """create a new name contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            node_id (int): name for the contract
            solution_provider_id (int, optional): solution provider id,

        Raises:
            RentContractCreationException: Rent contract creation failed

        Returns:
            int: contract ID
        """

        call = substrate.compose_call(
            "SmartContractModule",
            "create_rent_contract",
            {"node_id": node_id, "solution_provider_id": solution_provider_id},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise RentContractCreationException(call_response.error_message)

        return Contract.get_node_rent_contract_id(substrate, node_id)

    def get_node_rent_contract_id(substrate: SubstrateInterface, node_id: int):
        """get contract ID from name

        Args:
            substrate (SubstrateInterface): substrate instance
            node_id (int): node ID

        Raises:
            exp: Value error

        Returns:
            int: contract ID
        """

        contract_id = substrate.query("SmartContractModule", "ActiveRentContractForNode", [node_id])
        if contract_id == None:
            raise ValueError(f"can't get ID for a contract with node ID: {node_id}")

        return contract_id

    @staticmethod
    def set_contract_consumption(
        substrate: SubstrateInterface, identity: Identity, contract_id: int, resources: Resources
    ):
        """set contract consumption resources

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            contract_id (int): contract ID
            resources (Resources): consumption resources

        Raises:
            ContractConsumptionException: failed setting consumption resources

        Returns:
            _type_: _description_
        """
        call = substrate.compose_call(
            "SmartContractModule",
            "report_contract_resources",
            {"contract_id": contract_id, "resources": resources.__dict__},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise ContractConsumptionException(call_response.error_message)

    @staticmethod
    def cancel(substrate: SubstrateInterface, identity: Identity, contract_id: int):
        """cancel a deployment

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            contract_id (int): contract ID
        """

        call = substrate.compose_call("SmartContractModule", "cancel_contract", {"contract_id": contract_id})

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise ContractCancelException(call_response.error_message)

    @staticmethod
    def get(substrate: SubstrateInterface, contract_id: int):
        """get a contract

        Args:
            substrate (SubstrateInterface): substrate instance
            contract_id (int): contract ID
        """

        contract = substrate.query("SmartContractModule", "Contracts", [contract_id])
        if contract == None:
            raise ValueError(f"contract with id {contract_id} is not found")

        as_deleted_state = DeletedState(False, False)
        if contract["state"] == "Deleted":
            as_deleted_state = DeletedState(
                is_canceled_by_user=contract["state"]["is_canceled_by_user"].value,
                is_out_of_funds=contract["state"]["is_out_of_funds"].value,
            )
        
        grace_period_block_number = 0
        if contract["state"] == "GracePeriod":
            grace_period_block_number = contract["state"]["grace_period_block_number"].value
            
        contract_state = ContractState(
            is_created=contract["state"] == "Created",
            is_deleted=contract["state"] == "Deleted",
            as_deleted=as_deleted_state,
            is_grace_period=contract["state"] == "GracePeriod",
            as_grace_period_block_number=grace_period_block_number,
        )

        node_contract = NodeContract(0, None, "", 0, []) 
        if "NodeContract" in contract["contract_type"]:
            public_ips: list[PublicIP] = []
            for public_ip in contract["contract_type"].value["NodeContract"]["public_ips_list"]:
                public_ips.append(PublicIP(public_ip["ip"], public_ip["gw"], public_ip["contract_id"]))
                
            node_contract = NodeContract(
                node_id=contract["contract_type"].value["NodeContract"]["node_id"],
                deployment_hash=contract["contract_type"].value["NodeContract"]["deployment_hash"],
                deployment_data=contract["contract_type"].value["NodeContract"]["deployment_data"],
                public_ips_count=contract["contract_type"].value["NodeContract"]["public_ips"],
                public_ips=public_ips,
            )
            
        name_contract = NameContract("") 
        if "NameContract" in contract["contract_type"]:
            name_contract = NameContract(contract["contract_type"].value["NameContract"]["name"])
            
        rent_contract = RentContract(0) 
        if "RentContract" in contract["contract_type"]:
            node_contract = RentContract(contract["contract_type"].value["RentContract"]["node_id"])
        
        contract_type = ContractType(
            is_name_contract="NameContract" in contract["contract_type"],
            name_contract=name_contract,
            is_node_contract="NodeContract" in contract["contract_type"],
            node_contract=node_contract,
            is_rent_contract="RentContract" in contract["contract_type"],
            rent_contract=rent_contract,
        )

        return Contract(
            version=contract["version"].value,
            state=contract_state,
            twin_id=contract["twin_id"].value,
            contract_id=contract["contract_id"].value,
            contract_type=contract_type,
            solution_provider_id=contract["solution_provider_id"].value,
        )
