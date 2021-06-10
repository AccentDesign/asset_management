from django import forms

from app.forms.fields import UserModelChoiceField
from app.forms.widgets import DatePicker
from assets.models import Task, TaskHistory, TaskPriority, TaskType
from authentication.middleware.current_user import get_current_team
from authentication.models import User


class TaskForm(forms.ModelForm):
    initial_due_date = forms.DateField(
        widget=DatePicker,
        required=True
    )
    repeat_until = forms.DateField(
        widget=DatePicker,
        required=False
    )

    class Meta:
        model = Task
        exclude = ('asset', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = get_current_team().members
        self.fields['task_priority'].queryset = TaskPriority.for_team
        self.fields['task_type'].queryset = TaskType.for_team


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.for_team


class TaskListFilterForm(forms.Form):
    due_date = forms.DateField(
        widget=DatePicker,
    )
    assigned_to = UserModelChoiceField(
        queryset=User.objects.all(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = get_current_team().members
