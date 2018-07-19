from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin
from assets.models import TaskType


class TaskTypeList(LoginRequiredMixin, ListView):
    model = TaskType


class TaskTypeCreate(LoginRequiredMixin, CreateView):
    model = TaskType
    fields = '__all__'
    success_url = reverse_lazy('assets:task-type-list')


class TaskTypeUpdate(LoginRequiredMixin, UpdateView):
    model = TaskType
    fields = '__all__'
    success_url = reverse_lazy('assets:task-type-list')


class TaskTypeDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteView):
    model = TaskType
    success_url = reverse_lazy('assets:task-type-list')
