from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from app.views.mixins import ProtectedDeleteMixin
from assets.models import Contact


class ContactList(LoginRequiredMixin, ListView):
    model = Contact


class ContactCreate(LoginRequiredMixin, CreateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('assets:contact-list')


class ContactUpdate(LoginRequiredMixin, UpdateView):
    model = Contact
    fields = '__all__'
    success_url = reverse_lazy('assets:contact-list')


class ContactDelete(LoginRequiredMixin, ProtectedDeleteMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('assets:contact-list')
