from django.db import models
from AbstractSoftDelete.models import AbstractSoftDeleteModel
from courses.models import Courses
from content.models import PDFDocument

class Quizzes(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDFDocument , on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'quizzes'

    def __str__(self):        
        return self.title
