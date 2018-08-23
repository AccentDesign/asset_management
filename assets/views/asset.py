from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, DetailView
from mptt.exceptions import InvalidMove

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import AssetTaskFormset, AssetCopyForm, AssetForm
from assets.models import Asset
from authentication.views.mixins import ActivatedTeamRequiredMixin


class AssetRootList(ActivatedTeamRequiredMixin, ListView):
    model = Asset

    def get_queryset(self):
        return (
            super().get_queryset()
            .filter(parent__isnull=True)
            .select_related(
                'asset_type'
            )
        )


class AssetNodeList(ActivatedTeamRequiredMixin, DetailView):
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


class AssetCreate(ActivatedTeamRequiredMixin, SuccessMessageMixin, CreateView):
    model = Asset
    form_class = AssetForm
    formset_class = AssetTaskFormset
    success_message = 'created successfully'

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

        # save the formset
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

    def get_success_url(self):
        if self.object.is_child_node():
            return self.object.parent.get_nodes_url()
        return reverse_lazy('assets:asset-list')


class AssetUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    formset_class = AssetTaskFormset
    success_message = 'updated successfully'

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
        # a valid parent cannot be established until save using mptt
        # so catch the error raised by the asset form and return form_invalid
        try:
            self.object = form.save()
        except InvalidMove:
            return self.form_invalid(form, formset)

        # save the tasks
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

    def get_success_url(self):
        return self.object.get_nodes_url()


class AssetDelete(ActivatedTeamRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Asset
    success_url = reverse_lazy('assets:asset-list')

    def get_success_url(self):
        if self.object.is_child_node():
            return self.object.parent.get_nodes_url()
        return reverse_lazy('assets:asset-list')


class AssetCopy(ActivatedTeamRequiredMixin, SuccessMessageMixin, FormView):
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
        return reverse_lazy('assets:asset-update', kwargs={'pk': self.object.pk})
