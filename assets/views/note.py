from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import NoteForm, NoteSharedForm
from assets.models import Note
from authentication.middleware.current_user import get_current_user


class NoteList(LoginRequiredMixin, ListView):
    model = Note

    def get_queryset(self):
        return super().get_queryset().filter(user=get_current_user())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'shared_notes': self.request.user.shared_notes.all().select_related('user')
        })
        return context


class NoteCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    form_class = NoteForm
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:note-list')


class NoteUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Note
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:note-list')

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(user=get_current_user()) | Q(shared_users=get_current_user())
        )

    def get_form_class(self):
        if self.object.user == get_current_user():
            return NoteForm
        return NoteSharedForm


class NoteDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('assets:note-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=get_current_user())
