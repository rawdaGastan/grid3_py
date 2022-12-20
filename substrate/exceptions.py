"""
Exceptions module

- TwinCreationException
- TwinUpdateException

- AccountActivationFailed

- CapacityReservationContractCreationException
- CapacityReservationContractUpdateException
- NameCreationException
- ContractCancelException

- DeploymentCreationException
- DeploymentUpdateException
- DeploymentCancelException

- NodeCreationException
- NodeUpdateException
- NodeUpdateUptimeException

- FarmCreationException
"""


class GridException(Exception):
    def __init__(self, message, category=None, level=None, context=None):
        super().__init__(message)


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


class CapacityReservationContractCreationException(GridException):
    pass


class CapacityReservationContractUpdateException(GridException):
    pass


class NameCreationException(GridException):
    pass


class ContractCancelException(GridException):
    pass
