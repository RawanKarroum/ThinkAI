from django.db import models
from django.utils.timezone import now

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        # Override the default queryset to exclude soft-deleted objects
        return super().get_queryset().filter(deleted_at__isnull=True)

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

    
