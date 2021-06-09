from django import forms
from django.templatetags.static import static

from app.forms.formbuilder import FormBuilder


class DatePicker(forms.widgets.DateInput):
    def __init__(self, attrs=None, format=None):
        if not attrs:
            attrs = {
                'class': 'datepicker',
                'placeholder': 'yyyy-mm-dd'
            }
        if not format:
            format = '%Y-%m-%d'

        super().__init__(attrs, format)

    class Media:
        css = {
            'all': (
                static('ext/flatpickr/themes/primary.css'),
            )
        }
        js = (
            static('ext/flatpickr/flatpickr.js'),
            static('js/datepicker.js'),
        )


class FormBuilderWidget(forms.widgets.Input):
    template_name = 'forms/widgets/formbuilder.html'
    input_type = 'text'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update({
            'metadata': FormBuilder.metadata,
            'field_data_template': FormBuilder.field_data_template,
        })
        return context
