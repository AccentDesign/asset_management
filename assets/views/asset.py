from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import AssetTaskFormset, AssetCopyForm
from assets.models import Asset


class AssetList(LoginRequiredMixin, ListView):
    model = Asset


class AssetCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Asset
    fields = '__all__'
    formset_class = AssetTaskFormset
    success_message = 'created successfully'
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

        # create success message
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)


class AssetUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Asset
    fields = '__all__'
    formset_class = AssetTaskFormset
    success_message = 'updated successfully'
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

        # create success message
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)


class AssetDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('assets:asset-list')


class AssetCopy(LoginRequiredMixin, SuccessMessageMixin, FormView):
    form_class = AssetCopyForm
    object = None
    template_name = 'assets/asset_copy_form.html'

    def get_asset(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Asset, pk=pk)

    def get(self, request, *args, **kwargs):
        self.asset = self.get_asset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.asset = self.get_asset()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'asset': self.asset
        })
        return context

    def form_valid(self, form):
        self.object = self.asset.copy(parent=form.cleaned_data['copy_to'])
        messages.success(self.request, "copied successfully")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('assets:asset-update', kwargs={'pk': self.object.pk})
