"""node module"""

from dataclasses import dataclass


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
