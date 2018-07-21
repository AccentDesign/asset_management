from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin
from assets.forms import AssetTaskFormset
from assets.models import Asset


class AssetList(LoginRequiredMixin, ListView):
    model = Asset


class AssetCreate(LoginRequiredMixin, CreateView):
    model = Asset
    fields = '__all__'
    formset_class = AssetTaskFormset
    success_url = reverse_lazy('assets:asset-list')

    def get_formset(self, **kwargs):
        return self.formset_class(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = self.get_formset()
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = self.get_formset(data=request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial']['parent'] = self.request.GET.get('parent')
        return kwargs

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)


class AssetUpdate(LoginRequiredMixin, UpdateView):
    model = Asset
    fields = '__all__'
    formset_class = AssetTaskFormset
    success_url = reverse_lazy('assets:asset-list')

    def get_formset(self, **kwargs):
        return self.formset_class(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset(instance=self.object)
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = self.get_formset(data=request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)


class AssetDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('assets:asset-list')
