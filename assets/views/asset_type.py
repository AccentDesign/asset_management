from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import AssetType


class AssetTypeList(LoginRequiredMixin, ListView):
    model = AssetType


class AssetTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AssetType
    fields = '__all__'
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AssetType
    fields = '__all__'
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:asset-type-list')


class AssetTypeDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = AssetType
    success_url = reverse_lazy('assets:asset-type-list')
