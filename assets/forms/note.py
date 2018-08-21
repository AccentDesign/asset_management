from django import forms

from app.forms.widgets import CheckboxInputs
from assets.models import Note
from authentication.middleware.current_user import get_current_team


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {
            'shared_users': CheckboxInputs
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shared_users'].queryset = get_current_team().members


class NoteSharedForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('shared_users', )
