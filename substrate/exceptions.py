"""
Exceptions module

- TwinCreationException
- TwinUpdateException

- AccountActivationFailed

- NodeContractCreationException
- NodeContractUpdateException
- NameContractCreationException
- RentCreationCreationException
- ContractConsumptionException
- ContractCancelException

- DeploymentCreationException
- DeploymentUpdateException
- DeploymentCancelException

- NodeCreationException
- NodeUpdateException
- NodeUpdateUptimeException

- FarmCreationException

- RefundTransactionCreationOrAddingSigException
- SetRefundTransactionExecutedException

- ProposeOrVoteMintTransactionException
"""


class GridException(Exception):
    def __init__(self, message, category=None, level=None, context=None):
        super().__init__(message)


class ProposeOrVoteMintTransactionException(GridException):
    pass


class SetRefundTransactionExecutedException(GridException):
    pass


class RefundTransactionCreationOrAddingSigException(GridException):
    pass


class RentContractCreationException(GridException):
    pass


class ContractConsumptionException(GridException):
    pass


class RentCreationCreationException(GridException):
    pass


class NameContractCreationException(GridException):
    pass


class FarmCreationException(GridException):
    pass


class NodeCreationException(GridException):
    pass


class NodeUpdateException(GridException):
    pass


class NodeUpdateUptimeException(GridException):
    pass


class DeploymentCreationException(GridException):
    pass


class DeploymentUpdateException(GridException):
    pass


class DeploymentCancelException(GridException):
    pass


class TwinCreationException(GridException):
    pass


class TwinUpdateException(GridException):
    pass


class AccountActivationFailed(GridException):
    pass


class AcceptingTermsAndConditionsFailed(GridException):
    pass


class NodeContractCreationException(GridException):
    pass


class NodeContractUpdateException(GridException):
    pass


class NameCreationException(GridException):
    pass


class ContractCancelException(GridException):
    pass
