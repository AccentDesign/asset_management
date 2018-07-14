from django.db import models


class Asset(models.Model):
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
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
