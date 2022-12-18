"""Contract module"""

from substrateinterface import SubstrateInterface
from .identity import Identity


class Contract:
    def __init__(self, substrate: SubstrateInterface, identity: Identity):
        self.substrate = substrate
        self.identity = identity

    def create_capacity_reservation_contract(
        self, farm_id: int, policy: CapacityReservationPolicy, solution_provider_id: int
    ):
        call = self.substrate.compose_call(
            "SmartContractModule",
            "capacity_reservation_contract_create",
            {"farm": farm_id, "policy": policy, "provider_id": solution_provider_id},
        )
        # txID, target, types.U64(amount.Uint64()), signature, stellarAddress, sequence_number

        extrinsic = self.substrate.create_signed_extrinsic(call, self.identity.key_pair)
        blockHash = self.substrate.submit_extrinsic(extrinsic, True, True)

        print(blockHash)
