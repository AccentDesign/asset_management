from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

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
