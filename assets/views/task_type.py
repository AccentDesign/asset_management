from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import TaskType
from authentication.views.mixins import ActivatedTeamRequiredMixin


class TaskTypeList(ActivatedTeamRequiredMixin, ListView):
    model = TaskType


class TaskTypeCreate(ActivatedTeamRequiredMixin, SuccessMessageMixin, CreateView):
    model = TaskType
    fields = '__all__'
    success_message = 'created successfully'


class TaskTypeUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskType
    fields = '__all__'
    success_message = 'updated successfully'


class TaskTypeDelete(ActivatedTeamRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy('assets:task-type-list')
