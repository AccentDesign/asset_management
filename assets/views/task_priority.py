from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.models import TaskPriority


class TaskPriorityList(LoginRequiredMixin, ListView):
    model = TaskPriority


class TaskPriorityCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TaskPriority
    fields = '__all__'
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:task-priority-list')


class TaskPriorityUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TaskPriority
    fields = '__all__'
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:task-priority-list')


class TaskPriorityDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = TaskPriority
    success_url = reverse_lazy('assets:task-priority-list')
