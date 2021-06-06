from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import ContactForm
from assets.models import Contact
from authentication.views.mixins import ActivatedTeamRequiredMixin


class ContactList(ActivatedTeamRequiredMixin, ListView):
    model = Contact


class ContactCreate(ActivatedTeamRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:contact-list')


class ContactUpdate(ActivatedTeamRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:contact-list')


class ContactDelete(ActivatedTeamRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('assets:contact-list')
