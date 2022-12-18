"""
Exceptions module

- TwinCreationException
- TwinUpdateException
- AccountActivationFailed

"""


class GridException(Exception):
    def __init__(self, message, category=None, level=None, context=None):
        super().__init__(message)


class TwinCreationException(GridException):
    pass


class TwinUpdateException(GridException):
    pass


class AccountActivationFailed(GridException):
    pass


class AcceptingTermsAndConditionsFailed(GridException):
    pass
