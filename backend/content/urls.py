from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UploadPDFView

router = DefaultRouter()

urlpatterns = [
    path('upload-pdf/', UploadPDFView.as_view(), name='upload_pdf'),    
    path('', include(router.urls)),
]
