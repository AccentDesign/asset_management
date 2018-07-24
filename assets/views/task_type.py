from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import TaskType


class TaskTypeList(LoginRequiredMixin, ListView):
    model = TaskType


class TaskTypeCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TaskType
    fields = '__all__'
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:task-type-list')


class TaskTypeUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskType
    fields = '__all__'
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:task-type-list')


class TaskTypeDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy('assets:task-type-list')
