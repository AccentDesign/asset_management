from django import forms

from authentication.middleware.current_user import get_current_user
from authentication.models import Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = [
            'title'
        ]

    def save(self, commit=True):
        instance = super().save(commit)
        # add the admin by default as a member
        instance.members.add(get_current_user())
        return instance
