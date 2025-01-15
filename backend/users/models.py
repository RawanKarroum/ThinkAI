from django.db import models
from AbstractSoftDelete.models import AbstractSoftDeleteModel
from django.contrib.auth.models import AbstractUser

class Users(AbstractSoftDeleteModel, AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher')
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'users'