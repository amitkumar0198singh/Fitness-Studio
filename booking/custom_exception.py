from rest_framework import status
from rest_framework.exceptions import APIException


class CustomException(APIException):
    '''
    Base class for all custom exceptions
    '''
    status_code = False
    message = None
    detail = None

    def __init__(self, detail=None, message=None, status_code=None):
        self.detail = detail or self.detail
        self.message = message or self.message
        self.status_code = status_code or self.status_code



class DataNotFoundException(CustomException):
    message = "Data not found"
    status_code = status.HTTP_404_NOT_FOUND