from django import forms
from mptt.exceptions import InvalidMove
from mptt.forms import TreeNodeChoiceField

from app.forms.formsets import InlineFormSet
from assets.models import Asset, AssetType, Contact, Task
from .task import TaskForm


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset_type'].queryset = AssetType.objects
        self.fields['contact'].queryset = Contact.objects
        self.fields['parent'].queryset = Asset.objects

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_asset'].queryset = Asset.objects


AssetTaskFormset = forms.inlineformset_factory(
    Asset,
    Task,
    form=TaskForm,
    formset=InlineFormSet,
    extra=0,
    can_delete=True,
    can_order=False
)
