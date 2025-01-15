from rest_framework import viewsets
from .models import Users
from .serializers import UsersSerializer

class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Users.objects.all()
    serializer_class = UsersSerializer  
