from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Asset(MPTTModel):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    asset_type = models.ForeignKey(
        'assets.AssetType',
        on_delete=models.PROTECT
    )
    manufacturer = models.ForeignKey(
        'assets.Manufacturer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    serial_no = models.CharField(
        max_length=255,
        blank=True
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
