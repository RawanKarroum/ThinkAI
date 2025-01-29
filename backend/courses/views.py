from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Courses
from .serializers import CoursesSerializer

class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    # def get_queryset(self):
    #     """
    #     Filter courses based on the authenticated user's role.
    #     """
    #     user = self.request.user

    #     # Ensure the user is authenticated
    #     if not user.is_authenticated:
    #         return Courses.objects.none()

    #     # If the user is a teacher, return courses they teach
    #     if user.role == 'teacher':
    #         return Courses.objects.filter(teacher=user, deleted_at__isnull=True)

    #     # If the user is a student (if 'students' field exists), return courses they're enrolled in
    #     return Courses.objects.none()

    def get_queryset(self):
        """
        Return all courses, ignoring user authentication.
        """
        return Courses.objects.filter(deleted_at__isnull=True)