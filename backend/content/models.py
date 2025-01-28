from django.db import models
from adaptive_learning.storages import PDFStorage
from AbstractSoftDelete.models import AbstractSoftDeleteModel

class PDFDocument(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    file = models.FileField(storage=PDFStorage(), upload_to='')

    class Meta:
        db_table = 'pdf_documents'

    def __str__(self):
        return self.title
