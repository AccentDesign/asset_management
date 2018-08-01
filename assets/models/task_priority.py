from django.db import models
from django.urls import reverse_lazy


class TaskPriority(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'task priorities'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-priority-update', kwargs={'pk': self.pk})
