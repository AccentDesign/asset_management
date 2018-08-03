from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin, DeleteSuccessMessageMixin
from assets.forms import ContactForm
from assets.models import Contact


class ContactList(LoginRequiredMixin, ListView):
    model = Contact


class ContactCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Contact
    form_class = ContactForm
    success_message = 'created successfully'
    success_url = reverse_lazy('assets:contact-list')


class ContactUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form_class = ContactForm
    success_message = 'updated successfully'
    success_url = reverse_lazy('assets:contact-list')


class ContactDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('assets:contact-list')
