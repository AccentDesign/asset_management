from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import CreateView

from authentication.forms import TeamForm
from authentication.models import Team


class TeamCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Team
    form_class = TeamForm
    success_message = 'created successfully'

    def get_success_url(self):
        return '{}?team_pk={}'.format(reverse('home'), self.object.pk)
