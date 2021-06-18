from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from mptt.exceptions import InvalidMove

from app.forms.formbuilder import FormBuilder
from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import AssetCopyForm, AssetForm, AssetMoveForm
from assets.models import Asset
from authentication.views.mixins import ActivatedCollectionRequiredMixin


class AssetRootList(ActivatedCollectionRequiredMixin, ListView):
    model = Asset

    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(parent__isnull=True)
            .select_related(
                'asset_type'
            )
        )


class AssetNodeList(ActivatedCollectionRequiredMixin, DetailView):
    model = Asset
    template_name = 'assets/asset_list_nodes.html'

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related(
                'asset_type'
            )
            .prefetch_related(
                'children__asset_type'
            )
        )


class AssetCreate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Asset
    form_class = AssetForm
    success_message = 'created successfully'

    def get(self, request, *args, **kwargs):
        self.parent_asset = None
        if kwargs.get('asset_pk'):
            self.parent_asset = get_object_or_404(Asset, pk=kwargs.get('asset_pk'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.parent_asset = None
        if kwargs.get('asset_pk'):
            self.parent_asset = get_object_or_404(Asset, pk=kwargs.get('asset_pk'))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.parent_asset:
            context['parent_asset'] = self.parent_asset
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.parent = self.parent_asset
        self.object.save()

        # create success message
        success_message = self.get_success_message(form.cleaned_data)
        messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.object.is_child_node():
            if 'save_and_open' in self.request.POST:
                return self.object.get_nodes_url()
            return self.object.parent.get_nodes_url()
        return reverse_lazy('assets:asset-list')


class AssetUpdate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    success_message = 'updated successfully'

    def form_valid(self, form):
        # a valid parent cannot be established until save using mptt
        # so catch the error raised by the asset form and return form_invalid
        try:
            self.object = form.save()
        except InvalidMove:
            return self.form_invalid(form)

        # create success message
        success_message = self.get_success_message(form.cleaned_data)
        messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_nodes_url()


class AssetDelete(ActivatedCollectionRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('assets:asset-list')

    def get_success_url(self):
        if self.object.is_child_node():
            return self.object.parent.get_nodes_url()
        return reverse_lazy('assets:asset-list')


class AssetExtra(ActivatedCollectionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Asset
    success_message = 'updated successfully'
    template_name = 'assets/asset_extra_form.html'

    def get_form_class(self):
        return FormBuilder(self.object.asset_type.fields).get_form_class()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        del kwargs['instance']
        kwargs.update({'initial': self.object.extra_data})
        return kwargs

    def form_valid(self, form):
        self.object.extra_data = form.cleaned_data
        self.object.save()
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_nodes_url()


class AssetCopy(ActivatedCollectionRequiredMixin, SuccessMessageMixin, FormView):
    form_class = AssetCopyForm
    object = None
    template_name = 'assets/asset_copy_form.html'

    def get(self, request, *args, **kwargs):
        self.asset = self.get_asset()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.asset = self.get_asset()
        return super().post(request, *args, **kwargs)

    def get_asset(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Asset, pk=pk)

    def get_initial(self):
        return {'new_name': self.asset.name}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'asset': self.asset})
        return context

    def form_valid(self, form):
        self.object = self.asset.copy(
            name=form.cleaned_data['new_name'],
            parent=form.cleaned_data['parent_asset']
        )
        messages.success(self.request, "copied successfully")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_nodes_url()


class AssetMove(ActivatedCollectionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Asset
    form_class = AssetMoveForm
    template_name = 'assets/asset_move_form.html'

    def get_success_url(self):
        return self.object.get_nodes_url()
