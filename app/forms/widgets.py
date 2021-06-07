from django import forms
from django.templatetags.static import static


class DatePicker(forms.widgets.DateInput):
    def __init__(self, attrs=None, format=None):
        if not attrs:
            attrs = {
                'class': 'datepicker',
                'placeholder': 'dd/mm/yyyy'
            }
        if not format:
            format = '%d/%m/%Y'

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
