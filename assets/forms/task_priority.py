from django import forms

from assets.models import TaskPriority


class TaskPriorityForm(forms.ModelForm):
    class Meta:
        model = TaskPriority
        fields = '__all__'
        widgets = {
            'badge_colour': forms.widgets.TextInput(attrs={'type': 'color'}),
            'font_colour': forms.widgets.TextInput(attrs={'type': 'color'})
        }
