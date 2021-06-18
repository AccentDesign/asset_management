from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import TaskPriority
from authentication.views.mixins import ActivatedCollectionRequiredMixin


class TaskPriorityList(ActivatedCollectionRequiredMixin, ListView):
    model = TaskPriority


class TaskPriorityCreate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, CreateView):
    model = TaskPriority
    fields = '__all__'
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:task-priority-list')


class TaskPriorityUpdate(ActivatedCollectionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskPriority
    fields = '__all__'
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:task-priority-list')


class TaskPriorityDelete(ActivatedCollectionRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = TaskPriority
    success_url = reverse_lazy('assets:task-priority-list')
