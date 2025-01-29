from django.db import models
from django.conf import settings
from adaptive_learning.storages import PDFStorage
from AbstractSoftDelete.models import AbstractSoftDeleteModel
import boto3
from courses.models import Courses
from adaptive_learning.utils.s3_utils import generate_presigned_url

class PDFDocument(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    file = models.FileField(storage=PDFStorage(), upload_to='')  
    file_url = models.URLField(blank=True, null=True, max_length=1000) 
    course = models.ForeignKey(Courses , on_delete=models.CASCADE, null=True, blank=True) 
    extracted_text = models.TextField(blank=True, null=True)   

    class Meta:
        db_table = 'pdf_documents'

    def __str__(self):
        return self.title

    def generate_presigned_url(self):
        """
        Generate a presigned S3 URL for secure file access.
        """
        if not self.file:
            return None

        s3_key = f"pdfs/{self.file.name}"

        return generate_presigned_url(s3_key)

    def save(self, *args, **kwargs):
        """
        Override save method to store the presigned file URL after upload.
        """
        super().save(*args, **kwargs) 

        if self.file:
            self.file_url = self.generate_presigned_url()
            super().save(update_fields=['file_url']) 
