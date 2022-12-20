"""Contract module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface
from substrate.events import Event
from substrate.exceptions import (
    CapacityReservationContractCreationException,
    CapacityReservationContractUpdateException,
    ContractCancelException,
    NameCreationException,
)

from substrate.node import ConsumableResources, NodeFeatures, Resources
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
class NodePolicy:
    """node policy class"""

    node_id: int


@dataclass
class Exclusive:
    """exclusive class"""

    group_id: int
    resources: Resources
    features: OptionFeatures


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
class CapacityReservationPolicy:
    """Capacity reservation policy class"""

    is_any: bool
    as_any: Any
    is_exclusive: bool
    as_exclusive: Exclusive
    is_node: bool
    as_node: NodePolicy


@dataclass
class NameContract:
    """Name contract class"""

    name: str


@dataclass
class CapacityReservationContract:
    """Capacity reservation contract class"""

    node_id: int
    resources: ConsumableResources
    group_id: int
    public_ips: int
    deployments: list[int]


@dataclass
class ContractType:
    """Contract type class"""

    is_name_contract: bool
    name_contract: NameContract
    is_capacity_reservation_contract: bool
    capacity_reservation_contract: CapacityReservationContract


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
    def create_capacity_reservation_contract(
        substrate: SubstrateInterface,
        identity: Identity,
        farm_id: int,
        policy: CapacityReservationPolicy,
        solution_provider_id: int = 0,
    ):
        """create a new capacity reservation contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            farm_id (int): farm ID for the contract
            policy (CapacityReservationPolicy): capacity reservation policy
            solution_provider_id (int, optional): solution provider id
        """

        call = substrate.compose_call(
            "SmartContractModule",
            "capacity_reservation_contract_create",
            {"farm": farm_id, "policy": policy, "provider_id": solution_provider_id},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise CapacityReservationContractCreationException(call_response.error_message)

        contract_ids = Event.get_created_contract_ids(substrate, call_response)

        if len(contract_ids) == 0:
            raise CapacityReservationContractCreationException(
                "failed to get contract id after creating a capacity reservation contract"
            )

        return contract_ids[len(contract_ids) - 1]

    @staticmethod
    def update_capacity_reservation_contract(
        substrate: SubstrateInterface, identity: Identity, capacity_id: int, resources: Resources
    ):
        """update a capacity reservation contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            capacity_id (int): capacity reservation ID for the contract
            resources (Resources): capacity resources
        """

        call = substrate.compose_call(
            "SmartContractModule",
            "capacity_reservation_contract_update",
            {"capacity_id": capacity_id, "resources": resources},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise CapacityReservationContractUpdateException(call_response.error_message)

        contract_ids = Event.get_updated_contract_ids(substrate, call_response)

        if len(contract_ids) == 0:
            raise CapacityReservationContractUpdateException(
                "failed to get contract id after updating a capacity reservation contract"
            )

    @staticmethod
    def get_contract_id_by_name_registration(substrate: SubstrateInterface, name: str):
        """get contract ID from name

        Args:
            substrate (SubstrateInterface): substrate instance
            name (str): contract name

        Raises:
            exp: Value error

        Returns:
            int: contract ID
        """

        contract_id = substrate.query("SmartContractModule", "ContractIDByNameRegistration", [name])
        if contract_id == None:
            raise ValueError("can't get ID for a contract with name: " + name)

        return contract_id

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
    def get_capacity_reservation_contracts(substrate: SubstrateInterface, node_id: int):
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
    def create_name_contract(substrate: SubstrateInterface, identity: Identity, name: str):
        """create a new name contract

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            name (int): name for the contract
        """

        call = substrate.compose_call(
            "SmartContractModule",
            "create_name_contract",
            {"name": name},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise NameCreationException(call_response.error_message)

        return Contract.get_contract_id_by_name_registration(substrate, call_response)

    @staticmethod
    def cancel(substrate: SubstrateInterface, identity: Identity, contract_id: int):
        """cancel a deployment

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            contract_id (int): contract ID
        """

        call = substrate.compose_call("SmartContractModule", "cancel_contract", {"id": contract_id})

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

        as_deleted_state = DeletedState(
            is_canceled_by_user=contract["state"]["as_deleted"]["is_canceled_by_user"].value,
            is_out_of_funds=contract["state"]["as_deleted"]["is_out_of_funds"].value,
        )
        contract_state = ContractState(
            is_created=contract["state"]["is_created"].value,
            is_deleted=contract["state"]["is_deleted"].value,
            as_deleted=as_deleted_state,
            is_grace_period=contract["state"]["is_grace_period"].value,
            as_grace_period_block_number=contract["state"]["as_grace_period_block_number"].value,
        )

        name_contract = NameContract(contract["contract_type"]["name_contract"]["name"].value)

        capacity_reservation_contract_resources_total = Resources(
            hru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["total_resources"]["hru"].value,
            sru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["total_resources"]["sru"].value,
            cru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["total_resources"]["cru"].value,
            mru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["total_resources"]["mru"].value,
        )
        capacity_reservation_contract_resources_used = Resources(
            hru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["used_resources"]["hru"].value,
            sru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["used_resources"]["sru"].value,
            cru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["used_resources"]["cru"].value,
            mru=contract["contract_type"]["capacity_reservation_contract"]["resources"]["used_resources"]["mru"].value,
        )

        capacity_reservation_contract_resources = ConsumableResources(
            total_resources=capacity_reservation_contract_resources_total,
            used_resources=capacity_reservation_contract_resources_used,
        )

        deployments: list[int] = []
        for deployment_id in contract["contract_type"]["capacity_reservation_contract"]["deployments"].value:
            deployments.append(deployment_id)

        capacity_reservation_contract = CapacityReservationContract(
            node_id=contract["contract_type"]["capacity_reservation_contract"]["node_id"].value,
            resources=capacity_reservation_contract_resources,
            group_id=contract["contract_type"]["capacity_reservation_contract"]["group_id"].value,
            public_ips=contract["contract_type"]["capacity_reservation_contract"]["public_ips"].value,
            deployments=deployments,
        )

        contract_type = ContractType(
            is_name_contract=contract["contract_type"]["is_name_contract"].value,
            name_contract=name_contract,
            is_capacity_reservation_contract=contract["contract_type"]["is_capacity_reservation_contract"].value,
            capacity_reservation_contract=capacity_reservation_contract,
        )
        return Contract(
            version=contract["version"].value,
            state=contract_state,
            twin_id=contract["twin_id"].value,
            contract_type=contract_type,
            solution_provider_id=contract["solution_provider_id"].value,
        )
