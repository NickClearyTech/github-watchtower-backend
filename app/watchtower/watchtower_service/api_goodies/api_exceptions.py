from rest_framework.exceptions import APIException
from rest_framework import status

from django.utils.encoding import force_str


class InvalidParameterException(APIException):

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid use of parameter"
    default_code = "invalid_parameter"

    def __init__(self, parameter=None, error_message=None, code=None):
        if parameter is not None and error_message is not None:
            detail = force_str(f"Invalid use of parameter {parameter}: {error_message}")
            super().__init__(detail, code)
