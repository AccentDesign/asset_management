from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from assets.models import AssetType


class AssetTypeList(LoginRequiredMixin, ListView):
    model = AssetType


class AssetTypeCreate(LoginRequiredMixin, CreateView):
    model = AssetType
    fields = '__all__'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeUpdate(LoginRequiredMixin, UpdateView):
    model = AssetType
    fields = '__all__'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeDelete(LoginRequiredMixin, DeleteView):
    model = AssetType
    success_url = reverse_lazy('assets:asset-type-list')
