from django.db import models
from django.urls import reverse_lazy

from authentication.middleware.current_user import get_current_team


class TaskPriorityManager(models.Manager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        qs = super().get_queryset()

        team = get_current_team()

        if team:
            qs = qs.filter(team=team)

        return qs


class TaskPriority(models.Model):
    name = models.CharField(
        max_length=255
    )
    team = models.ForeignKey(
        'authentication.Team',
        on_delete=models.CASCADE,
        editable=False,
        default=get_current_team
    )

    objects = TaskPriorityManager()

    class Meta:
        ordering = ['name']
        unique_together = ('team', 'name', )
        verbose_name_plural = 'task priorities'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-priority-update', kwargs={'pk': self.pk})
