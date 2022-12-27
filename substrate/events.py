"""events class"""

from substrateinterface import SubstrateInterface

from dataclasses import dataclass
from substrate.event_records import EventRecords
from substrate.identity import Identity
from substrate.twin import Twin


@dataclass
class Block:
    """Block encoded with header and extrinsics"""

    header: dict
    extrinsics: list[dict]


@dataclass
class SignedBlock:
    """signed block class"""

    block: Block
    justification: bytes


@dataclass
class CallResponse:
    """call response class"""

    hash: bytes
    events: EventRecords
    block: SignedBlock
    identity: Identity


class Event:
    """event class"""

    @staticmethod
    def get_created_contract_ids(substrate: SubstrateInterface, call_response: CallResponse):
        """get created contracts' IDS

        Args:
            substrate (SubstrateInterface): substrate instance
            call_response (CallResponse): the extrinsic call response

        Raises:
            exp: Value error

        Returns:
            list[int]: list of contracts IDs
        """
        contract_ids: list[int] = []

        try:
            twin_id = Twin.get_twin_id_from_public_key(substrate, call_response.identity.public_key)
        except ValueError as exp:
            raise exp

        for e in call_response.events.SmartContractModule_ContractCreated:
            if e.contract.twin_id == twin_id:
                contract_ids.append(e.contract.contract_id)

        return contract_ids

    @staticmethod
    def get_created_deployments_ids(substrate: SubstrateInterface, call_response: CallResponse):
        """get created deployments' IDS

        Args:
            substrate (SubstrateInterface): substrate instance
            call_response (CallResponse): the extrinsic call response

        Raises:
            exp: Value error

        Returns:
            list[int]: list of deployments IDs
        """
        deployment_ids: list[int] = []

        try:
            twin_id = Twin.get_twin_id_from_public_key(substrate, call_response.identity.public_key)
        except ValueError as exp:
            raise exp

        for e in call_response.events.SmartContractModule_DeploymentCreated:
            if e.deployment.twin_id == twin_id:
                deployment_ids.append(e.deployment.id)

        return deployment_ids

    @staticmethod
    def get_updated_contract_ids(substrate: SubstrateInterface, call_response: CallResponse):
        """get updated contracts' IDS

        Args:
            substrate (SubstrateInterface): substrate instance
            call_response (CallResponse): the extrinsic call response

        Raises:
            exp: Value error

        Returns:
            list[int]: list of contracts IDs
        """
        contract_ids: list[int] = []

        try:
            twin_id = Twin.get_twin_id_from_public_key(substrate, call_response.identity.public_key)
        except ValueError as exp:
            raise exp

        for e in call_response.events.SmartContractModule_ContractUpdated:
            if e.contract.twin_id == twin_id:
                contract_ids.append(e.contract.contract_id)

        return contract_ids

    @staticmethod
    def get_updated_deployments(substrate: SubstrateInterface, call_response: CallResponse):
        """get updated deployments' IDS

        Args:
            substrate (SubstrateInterface): substrate instance
            call_response (CallResponse): the extrinsic call response

        Raises:
            exp: Value error

        Returns:
            list[int]: list of contracts IDs
        """
        deployment_ids: list[int] = []

        try:
            twin_id = Twin.get_twin_id_from_public_key(substrate, call_response.identity.public_key)
        except ValueError as exp:
            raise exp

        for e in call_response.events.SmartContractModule_DeploymentUpdated:
            if e.deployment.twin_id == twin_id:
                deployment_ids.append(e.deployment.id)

        return deployment_ids
