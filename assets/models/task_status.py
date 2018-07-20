from django.db import models


class TaskStatus(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'task statuses'

    def __str__(self):
        return self.name
