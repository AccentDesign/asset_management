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
            'all': ('//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css', )
        }
        js = (
            '//code.jquery.com/ui/1.12.1/jquery-ui.js',
            static('dist/js/datepicker.js'),
        )