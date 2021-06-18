from django.db import models
from django.urls import reverse_lazy

from .mixins import CollectionManager, CollectionMixin


class TaskPriorityManager(CollectionManager):
    pass


class TaskPriority(CollectionMixin):
    name = models.CharField(
        max_length=255
    )
    display_order = models.PositiveIntegerField(
        default=0,
    )

    for_collection = TaskPriorityManager()
    objects = models.Manager()

    class Meta:
        ordering = ['display_order']
        unique_together = ('collection', 'name', )
        verbose_name_plural = 'task priorities'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-priority-update', kwargs={'pk': self.pk})
