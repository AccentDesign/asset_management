from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from authentication.middleware.current_user import set_current_team


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if request.GET.get('team_pk'):
            set_current_team(request, request.GET.get('team_pk'))

        return response
