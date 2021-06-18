from copy import deepcopy

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.urls import reverse_lazy

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey

from .mixins import TeamManager, TeamMixin


class AssetManager(TeamManager, TreeManager):
    def search(self, query=None):
        """ Returns the search results for the main site search """

        qs = self.get_queryset()
        if query:
            all_filters = models.Q()
            for term in query.split():
                or_lookup = (
                    models.Q(name__icontains=term) |
                    models.Q(description__icontains=term) |
                    models.Q(asset_type__name__icontains=term) |
                    models.Q(contact__name__icontains=term)
                )
                all_filters = all_filters & or_lookup
            qs = qs.filter(all_filters).distinct()
        return qs


class Asset(TeamMixin, MPTTModel):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    asset_type = models.ForeignKey(
        'assets.AssetType',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    contact = models.ForeignKey(
        'assets.Contact',
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )
    extra_data = models.JSONField(
        default=dict,
        null=True,
        blank=True,
        encoder=DjangoJSONEncoder,
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    for_team = AssetManager()
    objects = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:asset-update', kwargs={'pk': self.pk})

    def get_nodes_url(self):
        return reverse_lazy('assets:asset-list-nodes', kwargs={'pk': self.pk})

    @property
    def extra_detail(self):
        if not self.asset_type:
            return

        return {
            v['label']: self.extra_data.get(k)
            for k, v in self.asset_type.fields.items()
        }

    def copy(self, **kwargs):
        """ Copy this asset and it's tasks """

        asset = Asset(
            name=kwargs.get('name', self.name),
            description=self.description,
            asset_type=self.asset_type,
            contact=self.contact,
            team=self.team,
            parent=kwargs.get('parent', self.parent)
        )

        asset.save()

        for task in self.tasks.all():
            new_task = deepcopy(task)
            new_task.pk = None
            new_task.asset = asset
            new_task.save()

        return asset

    copy.alters_data = True
