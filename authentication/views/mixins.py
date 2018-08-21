from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ActivatedTeamRequiredMixin(LoginRequiredMixin):
    """ Verify that the current user is authenticated and has an active team """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.activated_team:
            return redirect('')
        return super().dispatch(request, *args, **kwargs)
