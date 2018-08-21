import uuid

from django.db import models


class Status(models.Model):
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name
