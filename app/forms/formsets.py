from django.forms import BaseInlineFormSet
from django.forms.formsets import DELETION_FIELD_NAME

from app.forms.widgets import CheckboxInput


class InlineFormSet(BaseInlineFormSet):
    """ overridden to add the delete widget """

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields[DELETION_FIELD_NAME].widget = CheckboxInput()
