from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import QuizzesViewSet, GenerateQuizView

router = DefaultRouter()
router.register(r'quizzes', QuizzesViewSet)

urlpatterns = [
    path('generate-quiz/<int:pdf_id>/', GenerateQuizView.as_view(), name='generate_quiz'),
    path('', include(router.urls)),
]
