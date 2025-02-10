from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UploadPDFView, GetExtractedTextView


router = DefaultRouter()

urlpatterns = [
    path('upload-pdf/', UploadPDFView.as_view(), name='upload_pdf'),    
    path('extracted-text/<int:pdf_id>/', GetExtractedTextView.as_view(), name='extracted_text'),
    path('', include(router.urls)),
]
