from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import TaskPriority
from authentication.views.mixins import ActivatedTeamRequiredMixin


class TaskPriorityList(ActivatedTeamRequiredMixin, ListView):
    model = TaskPriority


class TaskPriorityCreate(ActivatedTeamRequiredMixin, SuccessMessageMixin, CreateView):
    model = TaskPriority
    fields = '__all__'
    success_message = 'created successfully'


class TaskPriorityUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskPriority
    fields = '__all__'
    success_message = 'updated successfully'


class TaskPriorityDelete(ActivatedTeamRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = TaskPriority
    success_url = reverse_lazy('assets:task-priority-list')
