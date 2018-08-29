import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from authentication.middleware.current_user import get_current_team, get_current_user


class FileManager(models.Manager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        qs = super().get_queryset()

        team = get_current_team()

        if team:
            qs = qs.filter(team=team)

        return qs


def get_upload_path(instance, filename):
    return f'files/{instance.team_id}/{filename}'


class File(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    file = models.FileField(
        upload_to=get_upload_path,
    )
    uploaded_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        default=get_current_user,
        editable=False
    )
    uploaded_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    team = models.ForeignKey(
        'authentication.Team',
        on_delete=models.CASCADE,
        editable=False,
        default=get_current_team
    )

    for_team = FileManager()
    objects = models.Manager()

    class Meta:
        ordering = ['file']

    def __str__(self):
        return self.file.name


@receiver(post_delete, sender=File)
def file_cleanup(instance, **kwargs):
    """ On post delete of a file remove from disk """

    instance.file.delete(False)
