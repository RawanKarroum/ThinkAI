from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager

class SoftDeleteManager(BaseUserManager):
    def get_queryset(self):
        # Override the default queryset to exclude soft-deleted objects
        return super().get_queryset().filter(deleted_at__isnull=True)
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class AbstractSoftDeleteModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager() # exclude soft deleted objects
    all_objects = models.Manager() # include all objects, even the soft deleted ones

    class Meta:
        abstract = True

    def delete(self):
        """
        Soft delete the object by setting `deleted_at` to the current time.
        """
        self.is_deleted = now()
        self.save()

    def restore(self, using=None):
        """
        Restore the soft-deleted object by setting `deleted_at` to None.
        """
        self.deleted_at = None  # Mark the object as active
        self.save(using=using)  # Save the restored object to the correct database

    @property
    def is_deleted(self):
        """
        Check if the object is soft deleted.
        """
        return self.deleted_at is not None

    
