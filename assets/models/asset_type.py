from django.db import models
from django.urls import reverse_lazy

from .mixins import CollectionManager, CollectionMixin


class AssetTypeManager(CollectionManager):
    pass


class AssetType(CollectionMixin):
    name = models.CharField(
        max_length=255
    )
    fields = models.JSONField(
        default=dict,
        null=True,
        blank=True,
    )

    for_collection = AssetTypeManager()
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = ('collection', 'name', )

    def get_absolute_url(self):
        return reverse_lazy('assets:asset-type-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
