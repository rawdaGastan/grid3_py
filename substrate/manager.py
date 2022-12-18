"""substrate client"""

from substrateinterface import SubstrateInterface

from substrate.account import Account
from substrate.twin import Twin
from .identity import Identity


class Client:
    """substrate client class"""

    def __init__(self, url: str, network=None):
        self.substrate = SubstrateInterface(url)
        self.manager = Manager(self)
        # self.deployer = Deployer(self)
        # self.deployment_builder = DeploymentBuilder()


class Manager:
    """substrate manager class"""

    def __init__(self, identity: Identity, substrate_url: str):
        self.substrate = SubstrateInterface(substrate_url)

        self.account = Account(self.substrate, identity)
        self.twin = Twin(self.substrate, identity)
