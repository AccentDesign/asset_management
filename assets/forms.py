from django import forms

from app.forms.widgets import DatePicker
from assets.models import Asset, Task


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
    extra=0,
    can_delete=True,
    can_order=False
)
