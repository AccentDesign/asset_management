import uuid

from django.db import models

from authentication.middleware.current_user import get_current_collection


class CollectionManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        collection = get_current_collection()
        if collection:
            qs = qs.filter(collection=collection)
        return qs


class CollectionMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    collection = models.ForeignKey(
        'authentication.Collection',
        on_delete=models.CASCADE,
        editable=False,
        default=get_current_collection
    )

    class Meta:
        abstract = True
