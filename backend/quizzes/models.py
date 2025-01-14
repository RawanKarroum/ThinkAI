from django.db import models
from AbstractSoftDelete.models import AbstractSoftDeleteModel
from courses.models import Courses

class Quizzes(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)

    def __str__(self):        
        return self.title
