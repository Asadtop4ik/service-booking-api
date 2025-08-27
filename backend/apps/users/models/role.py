from django.db import models

from apps.core.models import TimeStampedModel


class Role(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.name
