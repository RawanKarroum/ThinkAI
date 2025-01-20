import json
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import requests
import jwt
from jwt.algorithms import RSAAlgorithm

User = get_user_model()  

class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            print("🚨 No Authorization header found in request.")
            return None

        try:
            token = auth_header.split(" ")[1]  
            payload = self.decode_auth0_token(token)

            permissions = payload.get("https://thinkai-api/permissions", [])
            print(f"✅ Extracted Permissions: {permissions}")

            if "read:protected" not in permissions:
                print("🚨 User lacks the required 'read:protected' permission.")
                raise AuthenticationFailed("Permission denied.")

            sub = payload.get("sub")  
            email = payload.get("email", f"{sub}@auth0.com") 
            role = payload.get("https://thinkai-api/role", "student") 

            user, created = User.objects.get_or_create(
                username=sub,
                defaults={"email": email, "role": role}
            )

            user.jwt_payload = payload  
            return (user, None)

        except AuthenticationFailed as e:
            print(f"🚨 Authentication error: {e}")
            raise AuthenticationFailed(str(e))

    def decode_auth0_token(self, token):
        """Decode and verify the JWT token using Auth0's JWKS."""
        try:
            auth0_domain = settings.AUTH0_DOMAIN
            auth0_audience = settings.AUTH0_AUDIENCE

            jwks_url = f"https://{auth0_domain}/.well-known/jwks.json"
            print(f"📡 Fetching JWKS from: {jwks_url}")

            jwks = requests.get(jwks_url).json()
            print(f"🔑 JWKS Response: {jwks}")

            header = jwt.get_unverified_header(token)
            rsa_key = None

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

            if rsa_key is None:
                print("🚨 No matching key found in JWKS.")
                raise AuthenticationFailed("Invalid token: No matching key found.")

            public_key = RSAAlgorithm.from_jwk(json.dumps(rsa_key))

            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=auth0_audience,
                issuer=f"https://{auth0_domain}/"
            )

            print(f"✅ Successfully Decoded Token: {decoded_token}")  
            return decoded_token

        except jwt.ExpiredSignatureError:
            print("🚨 Token has expired.")
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError as e:
            print(f"🚨 Invalid token: {e}")
            raise AuthenticationFailed(f"Invalid token: {e}")
