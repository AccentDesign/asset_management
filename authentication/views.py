from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from authentication.models import User


class ProfileUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = (
        'email',
        'first_name',
        'last_name',
    )
    success_message = 'updated successfully'
    success_url = reverse_lazy('my_profile')

    def get_object(self, queryset=None):
        return self.request.user
