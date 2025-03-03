from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

User = get_user_model()

class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer  

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        user = request.user

        return Response({
            "message": "Access granted!",
            "user": user.username,
            "auth0_id": user.auth0_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role
        })
    
class GetUserRoleView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            auth0_id = request.data.get("auth0_id")
            if not auth0_id:
                return Response({"error": "Auth0 ID is required"}, status=400)
            
            user = User.objects.filter(auth0_id=auth0_id).first()
            if not user:
                    return Response({"error": "User not found"}, status=400)
            
            return Response({"role": user.role}, status=200)
        
        except Exception as e:
            print("❌ Error fetching user role:", str(e))
            return Response({"error": str(e)}, status=400)
    
class SaveUserView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        try:
            print("📡 Incoming Request Data:", request.data)  

            user_data = request.data  
            auth0_id = user_data.get("auth0_id")
            first_name = user_data.get("first_name", "").strip()
            last_name = user_data.get("last_name", "").strip()
            email = user_data.get("email")

            if not auth0_id:
                return Response({"error": "Auth0 ID is required"}, status=400)
            if not email:
                return Response({"error": "Email is required"}, status=400)

            user = User.objects.filter(auth0_id=auth0_id).first()

            if user:
                print("🔄 User already exists, updating details...")
                user.first_name = first_name if first_name else user.first_name
                user.last_name = last_name if last_name else user.last_name
                user.email = email
                user.username = email
                user.save()
                return Response({"message": "User updated successfully"}, status=200)

            user = User.objects.create(
                auth0_id=auth0_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                username=email
            )

            print("✅ New User Created:", user.auth0_id)
            return Response({"message": "User saved successfully"}, status=201)

        except Exception as e:
            print("❌ Error in SaveUserView:", str(e)) 
            return Response({"error": str(e)}, status=400)
