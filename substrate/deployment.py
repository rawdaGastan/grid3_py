"""Deployment module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface


from substrate.node import Resources
from substrate.identity import Identity
from substrate.events import Event
from substrate.exceptions import (
    DeploymentCancelException,
    DeploymentCreationException,
    DeploymentUpdateException,
)


@dataclass
class PublicIP:
    """Public IP class"""

    ip: str
    gateway: str
    contract_id: int


@dataclass
class Deployment:
    """Deployment class"""

    id: int
    twin_id: int
    capacity_reservation_id: int
    deployment_hash: bytes
    deployment_data: str
    public_ips_count: int
    public_ips: list[PublicIP]
    resources: Resources

    @staticmethod
    def create(
        substrate: SubstrateInterface,
        identity: Identity,
        capacity_reservation_contract_id: int,
        hash: bytes,
        data: str,
        resources: Resources,
        public_ips: int,
    ):
        """create a new deployment

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            capacity_reservation_contract_id (int): capacity reservation ID for the contract
            hash (Resources): deployment hash
            data (str): deployment data
            resources (Resources): deployment resources
            public_ips (int): if it has public ips 0/1
        """

        call = substrate.compose_call(
            "SmartContractModule",
            "deployment_create",
            {
                "capacity_reservation_contract_id": capacity_reservation_contract_id,
                "hash": hash,
                "data": data,
                "resources": resources,
                "public_ips": public_ips,
            },
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise DeploymentCreationException(call_response.error_message)

        deployment_ids = Event.get_created_deployments_ids(substrate, call_response)

        if len(deployment_ids) == 0:
            raise DeploymentCreationException("failed to get deployment id after creation")

        return deployment_ids[len(deployment_ids) - 1]

    @staticmethod
    def update(
        substrate: SubstrateInterface,
        identity: Identity,
        deployment_id: int,
        hash: bytes,
        data: str,
        resources: Resources,
    ):
        """update a deployment

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            deployment_id (int): deployment ID
            hash (Resources): deployment hash
            data (str): deployment data
            resources (Resources): deployment resources
            public_ips (int): if it has public ips 0/1
        """

        call = substrate.compose_call(
            "SmartContractModule",
            "deployment_update",
            {
                "id": deployment_id,
                "hash": hash,
                "data": data,
                "resources": resources,
            },
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise DeploymentUpdateException(call_response.error_message)

        deployment_ids = Event.get_updated_deployments_ids(substrate, call_response)

        if len(deployment_ids) == 0:
            raise DeploymentUpdateException("failed to get deployment id after creation")

        return deployment_ids[len(deployment_ids) - 1]

    @staticmethod
    def cancel(substrate: SubstrateInterface, identity: Identity, deployment_id: int):
        """cancel a deployment

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            deployment_id (int): deployment ID
        """

        call = substrate.compose_call("SmartContractModule", "deployment_cancel", {"id": deployment_id})

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise DeploymentCancelException(call_response.error_message)

    @staticmethod
    def get(substrate: SubstrateInterface, deployment_id: int):
        """get a deployment

        Args:
            substrate (SubstrateInterface): substrate instance
            deployment_id (int): deployment ID
        """

        deployment = substrate.query("SmartContractModule", "Deployments", [deployment_id])
        if deployment == None:
            raise ValueError("deployment with id " + id + "is not found")

        public_ips: list[PublicIP] = []
        for public_ip in deployment["public_ips"].value:
            public_ips.append(
                PublicIP(ip=public_ip["ip"], gateway=public_ip["gateway"], contract_id=public_ip["contract_id"])
            )

        resources = Resources(
            hru=deployment["resources"]["hru"].value,
            sru=deployment["resources"]["sru"].value,
            cru=deployment["resources"]["cru"].value,
            mru=deployment["resources"]["mru"].value,
        )

        return Deployment(
            id=deployment_id,
            twin_id=deployment["twin_id"].value,
            capacity_reservation_id=deployment["capacity_reservation_id"].value,
            deployment_hash=deployment["deployment_hash"].value,
            deployment_data=deployment["deployment_data"].value,
            public_ips_count=deployment["public_ips_count"].value,
            public_ips=public_ips,
            resources=resources,
        )
