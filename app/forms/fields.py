from django import forms
from django.core.exceptions import ValidationError

from app.forms.widgets import FormBuilderWidget
from app.forms.formbuilder import FormBuilder


class FormBuilderField(forms.JSONField):
    widget = FormBuilderWidget

    def validate(self, value):
        super().validate(value)
        # here we just try to generate a form with the value and render it
        # if it renders without error we know we can use the fields json ok
        try:
            FormBuilder(value).get_form_class()().as_p()
        except Exception:
            raise ValidationError("Invalid, please check all fields and try again.")


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()
