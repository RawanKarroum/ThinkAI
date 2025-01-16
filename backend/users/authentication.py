import json
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.header.get('Authorization')
    
        if not auth_header:
            return None
        
        token = auth_header.split(" ")[1]