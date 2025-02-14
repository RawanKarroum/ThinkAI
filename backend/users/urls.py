from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UsersViewSet, ProtectedView, SaveUserView

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename="users")

urlpatterns = [
    path('users/save', SaveUserView.as_view(), name='save_user'),
    path('users/protected/', ProtectedView.as_view(), name='protected'),
    path('', include(router.urls)),
]
