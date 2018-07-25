from django import forms

from app.forms.forms import InlineFormSet
from app.forms.widgets import DatePicker, CheckboxInputs
from assets.models import Asset, Task, TaskHistory, Note
from authentication.models import User


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


AssetTaskFormset = forms.inlineformset_factory(
    Asset,
    Task,
    form=TaskForm,
    formset=InlineFormSet,
    extra=0,
    can_delete=True,
    can_order=False
)


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
