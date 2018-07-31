from django import forms
from mptt.exceptions import InvalidMove
from mptt.forms import TreeNodeChoiceField

from app.forms.forms import InlineFormSet
from app.forms.widgets import DatePicker, CheckboxInputs
from assets.models import Asset, Task, TaskHistory, Note
from authentication.models import User


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'

    def save(self, commit=True):
        try:
            return super().save(commit)
        except InvalidMove as e:
            # catch an invalid parent node and re raise the error
            self.add_error('parent', e.args[0])
            raise


class AssetCopyForm(forms.Form):
    new_name = forms.CharField(
        max_length=255,
        help_text='Enter a new name for the asset.'
    )
    parent_asset = TreeNodeChoiceField(
        queryset=Asset.objects,
        required=False,
        help_text='Leave blank to make this a top level asset.'
    )


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
