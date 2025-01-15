from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CoursesViewSet

router = DefaultRouter()
router.register(r'courses', CoursesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
