from django.db import models
from django.urls import reverse_lazy

from simplemde.fields import SimpleMDEField

from authentication.middleware.current_user import get_current_team, get_current_user


class NoteManager(models.Manager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        qs = super().get_queryset()

        team = get_current_team()

        if team:
            qs = qs.filter(team=team)

        return qs


class Note(models.Model):
    title = models.CharField(
        max_length=255
    )
    content = SimpleMDEField(
        blank=True
    )
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        default=get_current_user,
        editable=False
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_on = models.DateTimeField(
        auto_now=True,
        editable=False
    )
    team = models.ForeignKey(
        'authentication.Team',
        on_delete=models.CASCADE,
        editable=False,
        default=get_current_team
    )

    objects = NoteManager()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('assets:note-update', kwargs={'pk': self.pk})
