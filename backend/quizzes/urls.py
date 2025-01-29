from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import QuizzesViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizzesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
