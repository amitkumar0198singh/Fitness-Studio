from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


from booking.custom_exception import CustomException


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, CustomException):
        return Response({"status": False, "message": exc.message, "detail": exc.detail}, status=exc.status_code)
    elif response is not None:
        response.data['status'] = False
    else:
        response = Response({"status": False, "message": "Something went wrong. Please try after some time",
                            'detail': str(exc) if exc else 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
