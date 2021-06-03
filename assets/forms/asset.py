from django import forms
from mptt.exceptions import InvalidMove
from mptt.forms import TreeNodeChoiceField

from assets.models import Asset, AssetType, Contact


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset_type'].queryset = AssetType.for_team
        self.fields['contact'].queryset = Contact.for_team
        self.fields['parent'].queryset = Asset.for_team

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
        queryset=Asset.for_team,
        required=False,
        help_text='Leave blank to make this a top level asset.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_asset'].queryset = Asset.for_team
