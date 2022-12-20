"""Farm module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface

from substrate.exceptions import FarmCreationException
from substrate.identity import Identity


@dataclass
class PublicIPInput:
    """Public IP input class"""

    ip: str
    gw: str


@dataclass
class PublicIP:
    """Public IP class"""

    ip: str
    gw: str
    contract_id: int


@dataclass
class FarmCertification:
    """Farm certification class"""

    is_gold: bool
    is_not_certified: bool


@dataclass
class FarmingPolicyLimit:
    """farming policy limit class"""

    farming_policy_id: int
    cu: int
    su: int
    end: int
    node_count: int
    node_certification: bool


@dataclass
class OptionFarmingPolicyLimit:
    """Option farming policy limit class"""

    has_value: bool
    as_value: FarmingPolicyLimit


@dataclass
class Farm:
    """Farm class"""

    version: int
    id: int
    name: str
    twin_id: int
    pricing_policy_id: int
    certification: FarmCertification
    public_ips: list[PublicIP]
    dedicated_farm: bool
    farming_policies_limit: OptionFarmingPolicyLimit

    def create(substrate: SubstrateInterface, identity: Identity, name: str, public_ips: list[PublicIPInput]):
        """create a new farm

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): farm's owner identity
            name (str): farm's name
            public_ips (list[PublicIPInput]): farm's public ips
        """
        farm_id = Farm.get_farm_id_by_name(substrate, name)
        if farm_id != 0:
            return farm_id

        call = substrate.compose_call(
            "TfgridModule",
            "create_farm",
            {"name": name, "public_ips": [i.__dict__ for i in public_ips]},
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success or call_response.error_message != None:
            raise FarmCreationException(call_response.error_message)

        return Farm.get_farm_id_by_name(substrate, name)

    @staticmethod
    def get(substrate: SubstrateInterface, farm_id: int):
        """get a farm by ID

        Args:
            substrate (SubstrateInterface): substrate instance
            farm_id (int): farm ID

        Raises:
            ValueError: farm is not found

        Returns:
            Node: farm object
        """

        farm = substrate.query("TfgridModule", "Farms", [farm_id])
        if farm == None:
            raise ValueError(f"farm with id {farm_id} is not found")

        certification = FarmCertification(
            is_gold=farm["certification"] == "Gold", is_not_certified=farm["certification"] == "NotCertified"
        )

        public_ips: list[PublicIP] = []
        for public_ip in farm["public_ips"]:
            public_ips.append(PublicIP(ip=public_ip["ip"], gw=public_ip["gw"], contract_id=public_ip["contract_id"]))

        farming_policies_limit = OptionFarmingPolicyLimit(False, None)
        if farm["farming_policy_limits"] != None:
            farming_policies_limit = OptionFarmingPolicyLimit(
                has_value=True,
                as_value=FarmingPolicyLimit(
                    farming_policy_id=farm["farming_policy_limits"]["farming_policy_id"],
                    cu=farm["farming_policy_limits"]["cu"],
                    su=farm["farming_policy_limits"]["su"],
                    end=farm["farming_policy_limits"]["end"],
                    node_count=farm["farming_policy_limits"]["node_count"],
                    node_certification=farm["farming_policy_limits"]["node_certification"],
                ),
            )

        return Farm(
            version=farm["version"].value,
            id=farm["id"].value,
            name=farm["name"].value,
            twin_id=farm["twin_id"].value,
            pricing_policy_id=farm["pricing_policy_id"].value,
            certification=certification,
            public_ips=public_ips,
            dedicated_farm=farm["dedicated_farm"].value,
            farming_policies_limit=farming_policies_limit,
        )

    @staticmethod
    def get_farm_id_by_name(substrate: SubstrateInterface, name: str):
        """get farm ID by name

        Args:
            substrate (SubstrateInterface): substrate instance
            name (str): farm's name

        Raises:
            ValueError: farm is not found

        Returns:
            int: farm ID
        """
        return substrate.query("TfgridModule", "FarmIdByName", [name])
