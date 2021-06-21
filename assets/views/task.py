from app.views.mixins import DeleteSuccessMessageMixin, ProtectedDeleteMixin
from assets.models.asset import Asset
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from assets.forms import TaskForm, TaskHistoryForm, TaskListFilterForm
from assets.models import Task, Status
from authentication.views.mixins import ActivatedCollectionRequiredMixin


class TaskList(ActivatedCollectionRequiredMixin, ListView):
    model = Task
    template_name = 'assets/task_list.html'

    def get_filter_form(self):
        if 'due_date' in self.request.GET:
            return TaskListFilterForm(self.request.GET)
        due_date = datetime.now().date() + timedelta(days=14)
        return TaskListFilterForm({'due_date': due_date})

    def get_queryset(self):
        filters = self.get_filter_form()

        if filters.is_valid():
            qs = Task.for_collection.due_by_date(
                date=filters.cleaned_data['due_date'],
                assigned_to=filters.cleaned_data.get('assigned_to')
            )
        else:
            qs = Task.for_collection.due_by_date()

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'filter_form': self.get_filter_form()
        })
        return context


class TaskCreate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    prefix = 'task_form'
    success_message = 'created successfully'

    def get(self, request, *args, **kwargs):
        self.asset = get_object_or_404(Asset, pk=kwargs.get('asset_pk'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.asset = get_object_or_404(Asset, pk=kwargs.get('asset_pk'))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asset'] = self.asset
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.asset = self.asset
        self.object.save()

        # create success message
        success_message = self.get_success_message(form.cleaned_data)
        messages.success(self.request, success_message)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.asset.get_nodes_url()


class TaskDetail(ActivatedCollectionRequiredMixin, SuccessMessageMixin, DetailView):
    model = Task

    def get_history_form(self):
        if self.request.method == 'POST':
            return TaskHistoryForm(self.request.POST)
        return TaskHistoryForm(initial={'task': self.object})

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_history_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_history_form()

        if form.is_valid():
            instance = form.save(commit=False)
            if 'complete' in self.request.POST:
                status, _ = Status.objects.get_or_create(name='Completed')
                instance.status = status
            instance.save()
            messages.success(request, 'notes added successfully')
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

    def get_success_url(self):
        return self.object.get_absolute_url()


class TaskUpdate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_message = 'updated successfully'

    def get_success_url(self):
        return self.object.get_absolute_url()


class TaskDelete(ActivatedCollectionRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Task

    def get_success_url(self):
        return self.object.asset.get_nodes_url()
