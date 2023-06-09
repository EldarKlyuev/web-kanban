import uuid
from django.db import models
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from kanban.settings import *

class User(models.Model):

    email = models.EmailField(max_length=255, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)

    GENDER_CHOICES = [
        ('Мужчина', 'Мужчина'),
        ('Женщина', 'Женщина'),
    ]

    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True)
    phone = models.CharField(max_length=20, blank=False)
    birthday = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)

    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]

    role_sys = models.CharField(max_length=20,
                                choices=ROLE_CHOICES, 
                                default=ROLE_CHOICES[1][1], 
                                null=True)

    is_enable = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)


    @property
    def token(self):
        """
        Generates access token and refresh token for the user
        """
        token_payload = {
            'id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + ACCESS_TOKEN_LIFETIME,
            'iat': datetime.utcnow(),
        }
        access_token = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm='HS256')
        token_payload = {
            'id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + REFRESH_TOKEN_LIFETIME,
            'iat': datetime.utcnow(),
        }
        refresh_token = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm='HS256')
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }

    def refresh_tokens(self):
        """
        Updates the access token and refresh token for the user
        """
        token_payload = {
            'id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + ACCESS_TOKEN_LIFETIME,
            'iat': datetime.utcnow(),
        }
        self.access_token = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm=ALGORITHM_JWT)
        token_payload = {
            'id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + REFRESH_TOKEN_LIFETIME,
            'iat': datetime.utcnow(),
        }
        self.refresh_token = jwt.encode(
            token_payload, settings.SECRET_KEY, algorithm=ALGORITHM_JWT)
        self.save()
        
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

class TokensVerify(models.Model):
    token_verify = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    token_verify_created_at = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey('User', on_delete=models.CASCADE)


class TokensReset(models.Model):
    token_reset = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    token_reset_created_at = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey('User', on_delete=models.CASCADE)


class TokensCompliteSignUp(models.Model):
    token_complite_signup = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True)
    token_complite_signup_created_at = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey('User', on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=50, blank=False)
    body = models.TextField(null=True, blank=True)
    workers = models.CharField(null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('Month plan', 'Month plan'),
        ('In work', 'In work'),
        ('In test', 'In test'),
        ('Done', 'Done'),
    ]

    status = models.CharField(max_length=255, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title
    
