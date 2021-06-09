import uuid

from django.db import models
from django.urls import reverse_lazy

from authentication.middleware.current_user import get_current_team


class AssetTypeManager(models.Manager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        qs = super().get_queryset()

        team = get_current_team()

        if team:
            qs = qs.filter(team=team)

        return qs


class AssetType(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        max_length=255
    )
    fields = models.JSONField(
        default=dict,
        null=True,
        blank=True,
    )
    team = models.ForeignKey(
        'authentication.Team',
        on_delete=models.CASCADE,
        editable=False,
        default=get_current_team
    )

    for_team = AssetTypeManager()
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = ('team', 'name', )

    def get_absolute_url(self):
        return reverse_lazy('assets:asset-type-update', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name
