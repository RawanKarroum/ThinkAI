from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        return Response({
            "message": "Access granted!",
            "user": request.user.username
        })
