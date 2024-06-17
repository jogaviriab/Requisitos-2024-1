from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from .models import Administrador

class AdminAuthentication(BaseBackend):
    def authenticate(self, request, email = None, password = None, **kwargs):
        try:
            user = Administrador.objects.get(correo=email)

            if user.check_password(password):
                return user
            else:
                return None
        except Administrador.DoesNotExist:
            return None
        
    def get_user(self, user_id:int):
        try:
            return Administrador.objects.get(pk=user_id)
        except Administrador.DoesNotExist:
            return None