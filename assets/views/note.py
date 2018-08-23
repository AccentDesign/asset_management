from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import NoteForm
from assets.models import Note
from authentication.views.mixins import ActivatedTeamRequiredMixin


class NoteList(ActivatedTeamRequiredMixin, ListView):
    model = Note


class NoteCreate(ActivatedTeamRequiredMixin, SuccessMessageMixin, CreateView):
    model = Note
    form_class = NoteForm
    success_message = 'created successfully'


class NoteUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Note
    form_class = NoteForm
    success_message = 'updated successfully'


class NoteDelete(ActivatedTeamRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Note
    success_url = reverse_lazy('assets:note-list')
