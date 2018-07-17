from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from assets.models import Asset


class AssetList(LoginRequiredMixin, ListView):
    model = Asset


class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('assets:asset-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        parent = self.request.GET.get('parent')
        if parent:
            kwargs['initial']['parent'] = parent
        return kwargs


class AssetUpdate(LoginRequiredMixin, UpdateView):
    model = Asset
    fields = '__all__'
    success_url = reverse_lazy('assets:asset-list')


class AssetDelete(LoginRequiredMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('assets:asset-list')
