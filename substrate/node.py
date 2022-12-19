"""node module"""

from dataclasses import dataclass
from substrate.contract import ConsumableResources
from substrateinterface import SubstrateInterface

@dataclass
class Resources:
    """resources class"""

    hru: int
    sru: int
    cru: int
    mru: int


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
class OptionBoardSerial:
    """Option board serial class"""

    has_value: bool
    as_value: str


@dataclass
class NodeCertification:
    """Node certification class"""

    is_diy: bool
    is_certified: bool


@dataclass
class Node:
    """Node class"""

    version: int
    id: int
    farm_id: int
    twin_id: int
    resources: ConsumableResources
    location: Location
    power: Power
    public_config: OptionPublicConfig
    Created: int
    FarmingPolicy: int
    interfaces: list[Interface]
    certification: NodeCertification
    secureBoot: bool
    virtualized: bool
    boardSerial: OptionBoardSerial
    connectionPrice: int
    
    @staticmethod
    def get_id_by_twin_id(substrate: SubstrateInterface, twin_id: int):
        """get node id by its twin id

        Args:
            substrate (SubstrateInterface): substrate instance
            twin_id (int): node's twin ID

        Raises:
            ValueError: node is not found

        Returns:
            int: node ID
        """
        node_id = substrate.query("TfgridModule", "NodeIdByTwinID", [twin_id])
        if node_id == None:
            raise ValueError("node with twin id " + twin_id + "is not found")
        
        return node_id
    
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
        if nodes == None:
            raise ValueError("nodes with farm id " + farm_id + "are not found")
        
        return nodes

