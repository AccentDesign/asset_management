from django import forms

from app.forms.widgets import DatePicker
from assets.models import Task, TaskHistory
from authentication.models import User


class TaskForm(forms.ModelForm):
    initial_due_date = forms.DateField(
        widget=DatePicker,
        input_formats=('%d/%m/%Y', ),
        required=True
    )
    repeat_until = forms.DateField(
        widget=DatePicker,
        input_formats=('%d/%m/%Y', ),
        required=False
    )

    class Meta:
        model = Task
        exclude = ('asset', )


class TaskHistoryForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.widgets.Textarea
    )

    class Meta:
        model = TaskHistory
        fields = ('task', 'notes', )
        widgets = {
            'task': forms.widgets.HiddenInput
        }


class TaskListFilterForm(forms.Form):
    due_date = forms.DateField(
        input_formats=('%d/%m/%Y', ),
        widget=DatePicker,
    )
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False
    )