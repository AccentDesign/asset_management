from django import forms

from app.forms.widgets import FormBuilderWidget
from app.forms.formbuilder import FormBuilder


class FormBuilderField(forms.JSONField):
    widget = FormBuilderWidget

    def validate(self, value):
        super().validate(value)
        FormBuilder(value).validate()


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()
