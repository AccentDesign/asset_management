from django.db import models
from django.urls import reverse_lazy


class AssetType(models.Model):
    name = models.CharField(
        max_length=255
    )

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse_lazy('assets:asset-type-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
