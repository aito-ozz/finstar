from enum import Enum


class GlobalErrorMessages(Enum):
    WRONG_STATUS_CODE = 'Received status code is not equal to expected'
    MATCHING_ERROR = 'XML does not match XSD'
    IS_NOT_DIGIT = 'The value is not a number'
    NON_EXISTENT_CURRENCY = 'There is no such currency code in the list'
