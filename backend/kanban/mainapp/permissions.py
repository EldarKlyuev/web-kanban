from rest_framework import permissions
from rest_framework.response import Response
from .models import *
import jwt
from django.conf import settings


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        token_user = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        request.token = token_user
        token = request.token
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_email = payload.get('email')
                user = User.objects.get(email=user_email)
                if payload.get('email') == user.email and user.role_sys == "Admin":
                    user.refresh_tokens()
                    return True
                
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                pass
        
        return False

class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        token_user = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
        request.token = token_user
        token = request.token
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_email = payload.get('email')
                user = User.objects.get(email=user_email)
                if payload.get('email') == user.email:
                    user.refresh_tokens()
                    return True
                
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                pass
        
        return False
    