from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static


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
                static('dist/css/jquery-ui.min.css'),
            )
        }
        js = (
            static('dist/js/jquery-ui.min.js'),
            static('dist/js/datepicker.js'),
        )
