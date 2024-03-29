from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import AssetTypeForm
from assets.models import AssetType
from authentication.views.mixins import ActivatedCollectionRequiredMixin


class AssetTypeList(ActivatedCollectionRequiredMixin, ListView):
    model = AssetType


class AssetTypeCreate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssetType
    form_class = AssetTypeForm
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeUpdate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AssetType
    form_class = AssetTypeForm
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeDelete(ActivatedCollectionRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = AssetType
    success_url = reverse_lazy('assets:asset-type-list')
