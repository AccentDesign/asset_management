from django.db import models
from django.urls import reverse_lazy

from .mixins import CollectionManager, CollectionMixin


class TaskTypeManager(CollectionManager):
    pass


class TaskType(CollectionMixin):
    name = models.CharField(
        max_length=255
    )

    for_collection = TaskTypeManager()
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = ('collection', 'name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-type-update', kwargs={'pk': self.pk})
