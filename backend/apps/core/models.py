from django.db import models


class TimeStampedModel(models.Model):
    """Abstract class for all models that adds datetime fields to write creation and updating time"""

    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
