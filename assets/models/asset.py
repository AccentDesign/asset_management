from copy import deepcopy

from django.db import models
from django.urls import reverse_lazy

from mptt.managers import TreeManager
from mptt.models import MPTTModel, TreeForeignKey


class AssetManager(TreeManager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        return super().get_queryset().annotate(
            qs_task_count=models.Count('tasks')
        )

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
    contact = models.ForeignKey(
        'assets.Contact',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    objects = AssetManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:asset-update', kwargs={'pk': self.pk})

    @property
    def task_count(self):
        """ Returns the count of tasks for this asset from AssetManager.get_queryset """

        return getattr(self, 'qs_task_count', None)

    def copy(self, **kwargs):
        """ Copy this asset and it's tasks """

        asset = Asset(
            name=kwargs.get('name', self.name),
            description=self.description,
            asset_type=self.asset_type,
            contact=self.contact,
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
