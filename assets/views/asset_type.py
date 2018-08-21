from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import AssetType
from authentication.views.mixins import ActivatedTeamRequiredMixin


class AssetTypeList(ActivatedTeamRequiredMixin, ListView):
    model = AssetType


class AssetTypeCreate(ActivatedTeamRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssetType
    fields = '__all__'
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AssetType
    fields = '__all__'
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeDelete(ActivatedTeamRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = AssetType
    success_url = reverse_lazy('assets:asset-type-list')
