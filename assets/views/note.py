from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.middleware.current_user import get_current_user
from assets.models import Note


class NoteList(LoginRequiredMixin, ListView):
    model = Note

    def get_queryset(self):
        return super().get_queryset().filter(user=get_current_user())


class NoteCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    fields = '__all__'
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:note-list')


class NoteUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Note
    fields = '__all__'
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:note-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=get_current_user())


class NoteDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('assets:note-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=get_current_user())
