from django import forms
from mptt.forms import TreeNodeChoiceField

from assets.models import Asset, AssetType, Contact


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        exclude = ('parent', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset_type'].queryset = AssetType.for_team
        self.fields['contact'].queryset = Contact.for_team


class AssetCopyForm(forms.Form):
    new_name = forms.CharField(
        max_length=255,
        help_text='Enter a new name for the asset.'
    )
    parent_asset = TreeNodeChoiceField(
        queryset=Asset.for_team,
        required=False,
        empty_label='Make it a root level asset'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent_asset'].queryset = Asset.for_team


class AssetMoveForm(forms.ModelForm):
    parent = TreeNodeChoiceField(
        queryset=Asset.for_team,
        required=False,
        empty_label='Make it a root level asset'
    )

    class Meta:
        model = Asset
        fields = ['parent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # remove from the qs all descendants of the instance as a node
        # cannot be moved to one of its descendants.
        descendants = self.instance.get_descendants(include_self=True)
        descendant_ids = descendants.values_list('id', flat=True)
        self.fields['parent'].queryset = Asset.for_team.exclude(id__in=descendant_ids)
