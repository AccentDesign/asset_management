import uuid

from django.db import models
from django.urls import reverse_lazy

from authentication.middleware.current_user import get_current_user


class Team(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=255,
        unique=True
    )
    admin = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=get_current_user
    )
    members = models.ManyToManyField(
        'authentication.User',
        blank=True,
        related_name='teams'
    )
    guests = models.ManyToManyField(
        'authentication.User',
        blank=True,
        related_name='guested_teams'
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('team-update', kwargs={'pk': self.pk})
