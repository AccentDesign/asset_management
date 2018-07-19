from django.db import models
from django.urls import reverse_lazy


class TaskType(models.Model):
    name = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-type-update', kwargs={'pk': self.pk})
