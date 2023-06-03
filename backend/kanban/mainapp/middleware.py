import jwt
from django.conf import settings
from .models import *

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token_user = request.META.get('HTTP_AUTHORIZATION', '')
        request.token = token_user
        response = self.get_response(request)
        return response