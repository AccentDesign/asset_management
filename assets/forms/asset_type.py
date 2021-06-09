from django import forms

from app.forms.fields import FormBuilderField
from assets.models import AssetType


class AssetTypeForm(forms.ModelForm):
    fields = FormBuilderField(
        required=False,
        initial=dict,
    )

    class Meta:
        model = AssetType
        fields = '__all__'
