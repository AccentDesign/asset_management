from django import forms

from authentication.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            'title'
        ]
