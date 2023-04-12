"""substrate client"""

from substrateinterface import SubstrateInterface

from substrate.account import Account
from substrate.bridge import RefundTransaction, MintTransaction
from substrate.contract import Contract
from substrate.farm import Farm
from substrate.twin import Twin
from substrate.node import Node
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

        self.account = Account
        self.twin = Twin
        self.farm = Farm
        self.node = Node
        self.contract = Contract
        self.refund_transaction = RefundTransaction
        self.mint_transaction = MintTransaction
