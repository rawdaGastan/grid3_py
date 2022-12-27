"""node module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface
from substrate.exceptions import NodeCreationException, NodeUpdateException, NodeUpdateUptimeException

from substrate.identity import Identity
from substrate.twin import Twin


@dataclass
class Resources:
    """resources class"""

    hru: int
    sru: int
    cru: int
    mru: int


@dataclass
class ConsumableResources:
    """Consumable resources class"""

    total_resources: Resources
    used_resources: Resources


@dataclass
class Location:
    """location class"""

    city: str
    country: str
    latitude: str
    longitude: str


@dataclass
class Role:
    """role class"""

    is_node: bool
    is_gateway: bool


@dataclass
class NodeFeatures:
    """node features class"""

    is_public_node: bool


@dataclass
class PowerTarget:
    """Power target class"""

    is_up: bool
    is_down: bool


@dataclass
class PowerState:
    """Power state class"""

    is_up: bool
    is_down: bool
    as_down: int


@dataclass
class OptionDomain:
    """Option domain class"""

    has_value: bool
    as_value: str


@dataclass
class IP:
    """IP"""

    ip: str
    gw: str


@dataclass
class OptionIP:
    """Option IP class"""

    has_value: bool
    as_value: IP


@dataclass
class PublicConfig:
    """Public config class"""

    ip4: IP
    ip6: OptionIP
    domain: OptionDomain


@dataclass
class OptionPublicConfig:
    """Option public config class"""

    has_value: bool
    as_value: PublicConfig


@dataclass
class Power:
    """Power class"""

    target: PowerTarget
    state: PowerState
    last_uptime: int


@dataclass
class Interface:
    """Interface class"""

    name: str
    mac: str
    ips: list[str]


@dataclass
class OptionSerial:
    """Option board serial class"""

    has_value: bool
    as_value: str


@dataclass
class NodeCertification:
    """Node certification class"""

    is_diy: bool
    is_certified: bool

    def __str__(self):
        if self.is_certified:
            return CERTIFIED
        return DIY


DIY = "Diy"
CERTIFIED = "Certified"


@dataclass
class Node:
    """Node class"""

    version: int
    id: int
    farm_id: int
    twin_id: int
    resources: Resources
    location: Location
    power: Power
    public_config: OptionPublicConfig
    created: int
    farming_policy: int
    interfaces: list[Interface]
    certification: NodeCertification
    secure_boot: bool
    virtualized: bool
    serial_number: OptionSerial
    connection_price: int

    @staticmethod
    def create(
        substrate: SubstrateInterface,
        identity: Identity,
        farm_id: int,
        resources: Resources,
        location: Location,
        interfaces: list[Interface],
        secure_boot: bool,
        virtualized: bool,
        serial_number: OptionSerial,
    ):
        """create a new node

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            farm_id (int): node farm's ID
            resources (Resources): node resources
            location (Location): node location
            interfaces (list[Interface]): node interfaces
            secure_boot (bool): node secure_boot
            virtualized (bool): node virtualized
            serial_number (OptionSerial): node serial_number

        Raises:
            NodeCreationException: Node creation failed

        Returns:
            int: node ID
        """
        twin_id = Twin.get_twin_id_from_public_key(substrate, identity.address)

        node_id = Node.get_id_by_twin_id(substrate, twin_id)
        if node_id != 0:
            return node_id

        call = substrate.compose_call(
            "TfgridModule",
            "create_node",
            {
                "farm_id": farm_id,
                "resources": resources.__dict__,
                "location": location.__dict__,
                "interfaces": [i.__dict__ for i in interfaces],
                "secure_boot": secure_boot,
                "virtualized": virtualized,
                "serial_number": serial_number.as_value,
            },
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success:
            raise NodeCreationException(call_response.error_message)

        return Node.get_id_by_twin_id(substrate, twin_id)

    @staticmethod
    def update(
        substrate: SubstrateInterface,
        identity: Identity,
        node_id: int,
        farm_id: int,
        resources: Resources,
        location: Location,
        interfaces: list[Interface],
        secure_boot: bool,
        virtualized: bool,
        serial_number: OptionSerial,
    ):
        """create a new node

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            node_id (int): node's ID
            farm_id (int): node farm's ID
            resources (Resources): node resources
            location (Location): node location
            interfaces (list[Interface]): node interfaces
            secure_boot (bool): node secure_boot
            virtualized (bool): node virtualized
            serial_number (OptionSerial): node serial_number

        Raises:
            NodeUpdateException: Node update failed
        """

        call = substrate.compose_call(
            "TfgridModule",
            "update_node",
            {
                "node_id": node_id,
                "farm_id": farm_id,
                "resources": resources.__dict__,
                "location": location.__dict__,
                "interfaces": [i.__dict__ for i in interfaces],
                "secure_boot": secure_boot,
                "virtualized": virtualized,
                "serial_number": serial_number.as_value,
            },
        )

        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success:
            raise NodeUpdateException(call_response.error_message)

        twin_id = Twin.get_twin_id_from_public_key(substrate, identity.address)
        return Node.get_id_by_twin_id(substrate, twin_id)

    @staticmethod
    def update_uptime(substrate: SubstrateInterface, identity: Identity, uptime: int):
        """update a node's uptime

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): contract's owner identity
            uptime (int): node's uptime
        """

        call = substrate.compose_call("TfgridModule", "report_uptime", {"uptime": uptime})
        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success:
            raise NodeUpdateUptimeException(call_response.error_message)

    @staticmethod
    def set_node_certificate(substrate: SubstrateInterface, identity: Identity, node_id: int, cert: NodeCertification):
        """set node certificate using its ID

        Args:
            substrate (SubstrateInterface): substrate instance
            identity (Identity): identity of the user
            node_id (int): node's ID
            cert (NodeCertification): certification

        Raises:
            NodeUpdateException: failed setting certification
        """
        call = substrate.compose_call(
            "TfgridModule", "set_node_certification", {"node_id": node_id, "node_certification": str(cert)}
        )
        extrinsic = substrate.create_signed_extrinsic(call, identity.key_pair)
        call_response = substrate.submit_extrinsic(extrinsic, True, True)

        if not call_response.is_success:
            raise NodeUpdateException(call_response.error_message)

    @staticmethod
    def get_id_by_twin_id(substrate: SubstrateInterface, twin_id: int):
        """get node id by its twin id

        Args:
            substrate (SubstrateInterface): substrate instance
            twin_id (int): node's twin ID

        Returns:
            int: node ID
        """
        return substrate.query("TfgridModule", "NodeIdByTwinID", [twin_id])

    @staticmethod
    def get_nodes_by_farm_id(substrate: SubstrateInterface, farm_id: int):
        """get nodes ids by their farm id

        Args:
            substrate (SubstrateInterface): substrate instance
            farm_id (int): node's farm ID

        Raises:
            ValueError: nodes are not found

        Returns:
            list[int]: nodes' IDs
        """
        nodes: list[int] = substrate.query("TfgridModule", "NodesByFarmID", [farm_id])
        if len(nodes) == 0:
            raise ValueError(f"nodes with farm id {farm_id} are not found")

        return nodes

    @staticmethod
    def get_last_node_id(substrate: SubstrateInterface):
        """get last nodes id

        Args:
            substrate (SubstrateInterface): substrate instance

        Raises:
            ValueError: last node ID is not found

        Returns:
            int: node ID
        """
        node_id: list[int] = substrate.query("TfgridModule", "NodeID")
        if node_id == 0:
            raise ValueError("last node ID is not found")

        return node_id

    @staticmethod
    def get(substrate: SubstrateInterface, node_id: int):
        """get a node

        Args:
            substrate (SubstrateInterface): substrate instance
            node_id (int): node ID

        Raises:
            ValueError: node is not found

        Returns:
            Node: node object
        """

        node = substrate.query("TfgridModule", "Nodes", [node_id])
        if node.value is None:
            raise ValueError(f"node with id {node_id} is not found")

        resources = Resources(
            hru=node["resources"]["hru"].value,
            sru=node["resources"]["sru"].value,
            cru=node["resources"]["cru"].value,
            mru=node["resources"]["mru"].value,
        )

        location = Location(
            city=node["location"]["city"].value,
            country=node["location"]["country"].value,
            latitude=node["location"]["latitude"].value,
            longitude=node["location"]["longitude"].value,
        )

        """TODO: power
        power = Power(
            target=PowerTarget(
                is_up=node["power"]["target"]["is_up"].value, is_down=node["power"]["target"]["is_down"].value
            ),
            state=PowerState(
                is_up=node["power"]["state"]["is_up"].value,
                is_down=node["power"]["state"]["is_down"].value,
                as_down=node["power"]["state"]["as_down"].value,
            ),
            last_uptime=node["power"]["last_uptime"].value,
        )
        """

        public_config = None
        if node["public_config"].value is not None:
            ip4 = IP(
                ip=node["public_config"]["ip4"]["ip"].value,
                gw=node["public_config"]["ip4"]["gw"].value,
            )

            ip6 = OptionIP(
                has_value=node["public_config"]["ip6"].value is not None,
                as_value=IP(
                    ip=node["public_config"]["ip6"]["ip"].value,
                    gw=node["public_config"]["ip6"]["gw"].value,
                ),
            )

            domain = OptionDomain(
                has_value=node["public_config"]["domain"].value is not None,
                as_value=node["public_config"]["domain"].value,
            )

            public_config = PublicConfig(ip4=ip4, ip6=ip6, domain=domain)

        interfaces: list[Interface] = []
        for interface in node["interfaces"]:
            interfaces.append(Interface(name=interface["name"], mac=interface["mac"], ips=interface["ips"]))

        certification = NodeCertification(
            is_diy=node["certification"] == "Diy", is_certified=node["certification"] == "Certified"
        )

        serial_number = OptionSerial(
            has_value=node["serial_number"].value is not None, as_value=node["serial_number"].value
        )

        return Node(
            version=node["version"].value,
            id=node["id"].value,
            farm_id=node["farm_id"].value,
            twin_id=node["twin_id"].value,
            resources=resources,
            location=location,
            power=None,  # TODO: power
            public_config=public_config,
            created=node["created"].value,
            farming_policy=node["farming_policy_id"].value,
            interfaces=interfaces,
            certification=certification,
            secure_boot=node["secure_boot"].value,
            virtualized=node["virtualized"].value,
            serial_number=serial_number,
            connection_price=node["connection_price"].value,
        )
