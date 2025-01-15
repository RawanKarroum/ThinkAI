from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Quizzes
from .serializers import QuizzesSerializer

class QuizzesViewSet(viewsets.ModelViewSet):
    queryset = Quizzes.objects.all()
    serializer_class = QuizzesSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    
    # def get_queryset(self):
    #     """
    #     Filter quizzes based on the authenticated user's role.
    #     """
    #     user = self.request.user

    #     # Ensure the user is authenticated
    #     if not user.is_authenticated:
    #         return Quizzes.objects.none()

    #     # If the user is a teacher, return quizzes for courses they teach
    #     if user.role == 'teacher':
    #         return Quizzes.objects.filter(course__teacher=user, deleted_at__isnull=True)

    #     # If the user is a student, return quizzes for courses they're enrolled in
    #     return Quizzes.objects.filter(course__students=user, deleted_at__isnull=True)

    def get_queryset(self):
        """
        Return all quizzes, ignoring user authentication.
        """
        return Quizzes.objects.filter(deleted_at__isnull=True)
