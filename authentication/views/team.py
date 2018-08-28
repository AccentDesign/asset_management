from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from app.views.mixins import DeleteSuccessMessageMixin
from authentication.forms import TeamForm
from authentication.middleware.current_user import set_current_team
from authentication.models import Team


class TeamActivate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        set_current_team(request, kwargs.get('pk'))
        return redirect('home')


class TeamCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Team
    form_class = TeamForm
    success_message = 'created successfully'

    def get_success_url(self):
        return reverse('team-activate', kwargs={'pk': self.object.pk})


class TeamUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Team
    form_class = TeamForm
    success_message = 'updated successfully'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        # only the admin of a team can update it
        return super().get_queryset().filter(admin=self.request.user)


class TeamDelete(LoginRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Team
    success_url = reverse_lazy('home')

    def get_queryset(self):
        # only the admin of a team can delete it
        return super().get_queryset().filter(admin=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        # delete anything that would stop this from being deleted first
        self.object.asset_set.all().delete()
        # delete team then redirect home
        self.object.delete()
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)
