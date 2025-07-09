import json

from django.utils.deprecation import MiddlewareMixin

from booking.utils import get_ip_address


class LogRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            print("\n========================= Request Data =========================")
            print(f"Request path : {request.path}")
            print(f"Request method : {request.method}")
            print(f"Request content type : {request.content_type}")
            print(f"Request user : {request.user}")
            print(f"Request IP : {get_ip_address(request)}")
            print(f"Request origin : {request.META.get('HTTP_ORIGIN')}")
            if request.content_type == 'text/plain':
                print("Request body : No body found (text/plain)")
            elif request.content_type == 'multipart/form-data':
                print("Request body : Body in form data (multipart)")
            elif request.content_type == 'application/json':
                print(f"Request body : {json.loads(request.body)}")
            else:
                print(f"Request body : {request.body}")
        except Exception:
            import traceback
            traceback.print_exc()

    def process_response(self, request, response):
        try:
            print("\n========================= Response Data =========================")
            print(f"Response status code : {response.status_code}")
            print(f"Response body : {json.loads(response.content)}")
        except Exception:
            import traceback
            traceback.print_exc()
        return response