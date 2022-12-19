"""events records module"""

from dataclasses import dataclass
from substrateinterface import SubstrateInterface

from substrate.contract import Contract
from substrate.deployment import Deployment


@dataclass
class Phase:
    """Phase is a class describing the current phase of the event (applying the extrinsic or finalized)"""

    is_applyExtrinsic: bool
    as_applyExtrinsic: int
    is_finalization: bool
    is_initialization: bool


@dataclass
class ContractCreated:
    """Contract created event class"""

    phase: Phase
    contract: Contract
    topics: list[bytes]


@dataclass
class ContractUpdated:
    """Contract updated event class"""

    phase: Phase
    contract: Contract
    topics: list[bytes]


@dataclass
class NodeContractCanceled:
    """Node contract canceled event class"""

    Phase: Phase
    contract_id: int
    node_id: int
    twin_id: id
    topics: list[bytes]


@dataclass
class NameContractCanceled:
    """Name contract canceled event class"""

    Phase: Phase
    contract_id: int
    topics: list[bytes]


@dataclass
class ContractDeployed:
    """Contract deployed event class"""

    Phase: Phase
    contract_id: int
    account_id: bytes
    topics: list[bytes]


@dataclass
class DeploymentCreated:
    """Deployment created event class"""

    phase: Phase
    deployment: Deployment
    topics: list[bytes]


@dataclass
class DeploymentUpdated:
    """Deployment updated event class"""

    phase: Phase
    deployment: Deployment
    topics: list[bytes]


@dataclass
class DeploymentCanceled:
    """Deployment canceled event class"""

    phase: Phase
    deployment_id: int
    twin_id: int
    node_id: int
    capacity_reservation_id: int
    topics: list[bytes]


@dataclass
class EventRecords:
    """event records class"""

    # types.EventRecords

    #########################
    # Smart contract module #
    #########################

    SmartContractModule_ContractCreated: list[ContractCreated]
    SmartContractModule_ContractUpdated: list[ContractUpdated]
    SmartContractModule_NameContractCanceled: list[NameContractCanceled]
    SmartContractModule_IPsReserved: list[IPsReserved]
    SmartContractModule_IPsFreed: list[IPsFreed]
    SmartContractModule_ContractDeployed: list[ContractDeployed]
    SmartContractModule_ConsumptionReportReceived: list[ConsumptionReportReceived]
    SmartContractModule_ContractBilled: list[ContractBilled]
    SmartContractModule_TokensBurned: list[TokensBurned]
    SmartContractModule_UpdatedUsedResources: list[UpdatedUsedResources]
    SmartContractModule_NruConsumptionReportReceived: list[NruConsumptionReportReceived]
    SmartContractModule_RentContractCanceled: list[RentContractCanceled]
    SmartContractModule_ContractGracePeriodStarted: list[ContractGracePeriodStarted]
    SmartContractModule_ContractGracePeriodEnded: list[ContractGracePeriodEnded]
    SmartContractModule_NodeMarkedAsDedicated: list[NodeMarkAsDedicated]
    SmartContractModule_SolutionProviderCreated: list[SolutionProviderCreated]
    SmartContractModule_SolutionProviderApproved: list[SolutionProviderApproved]
    SmartContractModule_GroupCreated: list[GroupCreated]
    SmartContractModule_GroupDeleted: list[GroupDeleted]
    SmartContractModule_CapacityReservationContractCanceled: list[CapacityReservationContractCanceled]
    SmartContractModule_DeploymentCreated: list[DeploymentCreated]
    SmartContractModule_DeploymentUpdated: list[DeploymentUpdated]
    SmartContractModule_DeploymentCanceled: list[DeploymentCanceled]

    ###################
    # TF grid module #
    ###################

    # farm events
    TfgridModule_FarmStored: list[FarmStored]
    TfgridModule_FarmUpdated: list[FarmStored]
    TfgridModule_FarmDeleted: list[FarmDeleted]

    # node events
    TfgridModule_NodeStored: list[NodeStored]
    TfgridModule_NodeUpdated: list[NodeStored]
    TfgridModule_NodeDeleted: list[NodeDeleted]
    TfgridModule_NodeUptimeReported: list[NodeUptimeReported]
    TfgridModule_NodePublicConfigStored: list[NodePublicConfig]
    TfgridModule_PowerTargetChanged: list[PowerTargetChanged]
    TfgridModule_PowerStateChanged: list[PowerStateChanged]

    # entity events
    TfgridModule_EntityStored: list[EntityStored]
    TfgridModule_EntityUpdated: list[EntityStored]
    TfgridModule_EntityDeleted: list[EntityDeleted]

    # twin events
    TfgridModule_TwinStored: list[TwinStored]
    TfgridModule_TwinUpdated: list[TwinStored]
    TfgridModule_TwinDeleted: list[TwinDeleted]
    TfgridModule_TwinEntityStored: list[TwinEntityStored]
    TfgridModule_TwinEntityRemoved: list[TwinEntityRemoved]

    # policy events
    TfgridModule_PricingPolicyStored: list[PricingPolicyStored]
    TfgridModule_FarmingPolicyStored: list[FarmingPolicyStored]

    # other events
    TfgridModule_FarmPayoutV2AddressRegistered: list[FarmPayoutV2AddressRegistered]
    TfgridModule_FarmMarkedAsDedicated: list[FarmMarkedAsDedicated]
    TfgridModule_ConnectionPriceSet: list[ConnectionPriceSet]
    TfgridModule_NodeCertificationSet: list[NodeCertificationSet]
    TfgridModule_NodeCertifierAdded: list[NodeCertifierAdded]
    TfgridModule_NodeCertifierRemoved: list[NodeCertifierRemoved]
    TfgridModule_FarmingPolicyUpdated: list[FarmingPolicyUpdated]
    TfgridModule_FarmingPolicySet: list[FarmingPolicySet]
    TfgridModule_FarmCertificationSet: list[FarmCertificationSet]
    TfgridModule_ZosVersionUpdated: list[ZosVersionUpdated]

    ##################
    # Burning module #
    ##################

    BurningModule_BurnTransactionCreated: list[BurnTransactionCreated]

    #####################
    # TFT bridge module #
    #####################

    # mints
    TFTBridgeModule_MintTransactionProposed: list[MintTransactionProposed]
    TFTBridgeModule_MintTransactionVoted: list[MintTransactionVoted]
    TFTBridgeModule_MintCompleted: list[MintCompleted]
    TFTBridgeModule_MintTransactionExpired: list[MintTransactionExpired]

    # burns
    TFTBridgeModule_BurnTransactionCreated: list[BridgeBurnTransactionCreated]
    TFTBridgeModule_BurnTransactionProposed: list[BurnTransactionProposed]
    TFTBridgeModule_BurnTransactionSignatureAdded: list[BurnTransactionSignatureAdded]
    TFTBridgeModule_BurnTransactionReady: list[BurnTransactionReady]
    TFTBridgeModule_BurnTransactionProcessed: list[BurnTransactionProcessed]
    TFTBridgeModule_BurnTransactionExpired: list[BridgeBurnTransactionExpired]

    # refunds
    TFTBridgeModule_RefundTransactionCreated: list[RefundTransactionCreated]
    TFTBridgeModule_RefundTransactionsignatureAdded: list[RefundTransactionSignatureAdded]
    TFTBridgeModule_RefundTransactionReady: list[RefundTransactionReady]
    TFTBridgeModule_RefundTransactionProcessed: list[RefundTransactionProcessed]
    TFTBridgeModule_RefundTransactionExpired: list[RefundTransactionCreated]

    ###################
    # TFTPrice module #
    ###################

    TFTPriceModule_PriceStored: list[PriceStored]
    TFTPriceModule_AveragePriceStored: list[PriceStored]
    TFTPriceModule_OffchainWorkerExecuted: list[OffchainWorkerExecuted]
    TFTPriceModule_AveragePriceIsAboveMaxPrice: list[AveragePriceIsAboveMaxPrice]
    TFTPriceModule_AveragePriceIsBelowMinPrice: list[AveragePriceIsAboveMinPrice]

    ##################
    # KVStore module #
    ##################

    TFKVStore_EntrySet: list[EntryEvent]
    TFKVStore_EntryGot: list[EntryEvent]
    TFKVStore_EntryTaken: list[EntryEvent]

    ########################
    # Validator set pallet #
    ########################

    ValidatorSet_ValidatorAdditionInitiated: list[ValidatorAdded]
    ValidatorSet_ValidatorRemovalInitiated: list[ValidatorRemoved]

    Validator_Bonded: list[Bonded]
    Validator_ValidatorRequestCreated: list[ValidatorCreated]
    Validator_ValidatorRequestApproved: list[ValidatorApproved]
    Validator_ValidatorActivated: list[ValidatorApproved]
    Validator_ValidatorRemoved: list[ValidatorApproved]
    Validator_NodeValidatorChanged: list[Bonded]
    Validator_NodeValidatorRemoved: list[Bonded]

    #############################
    # Council membership pallet #
    #############################

    CouncilMembership_MemberAdded: list[MemberEvent]
    CouncilMembership_MemberRemoved: list[MemberEvent]
    CouncilMembership_MembersSwapped: list[MemberEvent]
    CouncilMembership_MembersReset: list[MemberEvent]
    CouncilMembership_KeyChanged: list[MemberEvent]
    CouncilMembership_Dummy: list[MemberEvent]

    ##############
    # Dao pallet #
    ##############

    Dao_Voted: list[Voted]
    Dao_Proposed: list[Proposed]
    Dao_Approved: list[Approved]
    Dao_Disapproved: list[Disapproved]
    Dao_Executed: list[Executed]
    Dao_Closed: list[Closed]
    Dao_ClosedByCouncil: list[ClosedByCouncil]
    Dao_CouncilMemberVeto: list[CouncilMemberVeto]
