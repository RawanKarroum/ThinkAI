from django.db import models
from AbstractSoftDelete.models import AbstractSoftDeleteModel
from users.models import Users

class Courses(AbstractSoftDeleteModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return self.title
