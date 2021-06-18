from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect


class ActivatedCollectionRequiredMixin(LoginRequiredMixin):
    """ Verify that the current user is authenticated and has an active collection """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.activated_collection:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
