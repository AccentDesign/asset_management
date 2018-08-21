from django.db import models
from django.urls import reverse_lazy

from simplemde.fields import SimpleMDEField

from authentication.middleware.current_user import get_current_user


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
    shared_users = models.ManyToManyField(
        'authentication.User',
        blank=True,
        related_name='shared_notes'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('assets:note-update', kwargs={'pk': self.pk})
