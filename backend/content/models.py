from django.db import models
from django.conf import settings
from adaptive_learning.storages import PDFStorage
from AbstractSoftDelete.models import AbstractSoftDeleteModel
import boto3

class PDFDocument(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    file = models.FileField(storage=PDFStorage(), upload_to='')  
    file_url = models.URLField(blank=True, null=True, max_length=1000) 

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
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION
        )

        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=3600 
        )

        return presigned_url

    def save(self, *args, **kwargs):
        """
        Override save method to store the presigned file URL after upload.
        """
        super().save(*args, **kwargs) 

        if self.file:
            self.file_url = self.generate_presigned_url()
            super().save(update_fields=['file_url']) 
