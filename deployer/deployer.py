"""Deployer module"""

from dataclasses import dataclass
from substrate.identity import Identity


@dataclass
class Deployer:
    identity: Identity
