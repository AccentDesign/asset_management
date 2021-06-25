import os
import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from authentication.middleware.current_user import get_current_user, get_current_collection


class AssetFileManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        collection = get_current_collection()
        if collection:
            qs = qs.filter(asset__collection=collection)
        return qs


def get_upload_path(instance, filename):
    return f'files/{instance.asset_id}/{filename}'


class AssetFile(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(
        upload_to=get_upload_path,
    )
    uploaded_by = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        default=get_current_user
    )
    uploaded_on = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    for_collection = AssetFileManager()
    objects = models.Manager()

    class Meta:
        ordering = ['file']

    def __str__(self):
        return self.file.name

    def filename(self):
        return os.path.basename(self.file.name)

    def filesize(self):
        return self.file.size

    def fileurl(self):
        return self.file.url


@receiver(post_delete, sender=AssetFile)
def file_cleanup(instance, **kwargs):
    """ On post delete of a file remove from disk """

    instance.file.delete(False)
