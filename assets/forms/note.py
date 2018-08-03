from django import forms

from app.forms.widgets import CheckboxInputs
from assets.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {
            'shared_users': CheckboxInputs
        }


class NoteSharedForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ('shared_users', )
