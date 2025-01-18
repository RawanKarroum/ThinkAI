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

        try:
            payload = self.decode_auth0_token(token)
            return (payload, None)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(str(e))
        
    def decode_auth0_token(self, token):
        url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"

        try:
            response = requests.get(url)
            response.raise_for_status()
            jwks = response.json()
            return self.verify_jwt(token, jwks)
        except requests.exceptions.RequestException as e:
            raise AuthenticationFailed("Auth0 token verification failed.")
        
    def verify_jwt(self, token, jwks):
        try:
            header = jwt.get_unverified_header(token)
            rsa_key = {}

            for key in jwks["keys"]:
                if key["kid"] == header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
                    break

                if not rsa_key:
                    raise AuthenticationFailed("Invalid token: No matching key found.")
                
                public_key = RSAAlgorithm.from_jwk(json.dumps(rsa_key))

                decoded_token = jwt.decode(
                    token, 
                    public_key, 
                    algorithms=["RS256"],
                    audience=settings.AUTH0_AUDIENCE,
                    issuer=f"https://{settings.AUTH0_DOMAIN}/"
                )
                return decoded_token
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")
                
