from django.db import models
from django.urls import reverse_lazy

from .mixins import TeamManager, TeamMixin


class TaskTypeManager(TeamManager):
    pass


class TaskType(TeamMixin):
    name = models.CharField(
        max_length=255
    )

    for_team = TaskTypeManager()
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = ('team', 'name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-type-update', kwargs={'pk': self.pk})
