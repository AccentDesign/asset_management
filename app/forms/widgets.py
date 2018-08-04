from django import forms
from django.contrib.staticfiles.templatetags.staticfiles import static


class CheckboxInput(forms.widgets.CheckboxInput):
    template_name = 'app/forms/widgets/checkbox_input.html'


class CheckboxInputs(forms.widgets.CheckboxSelectMultiple):
    option_template_name = 'app/forms/widgets/checkbox_option.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'list-style-none'
        return context


class ClearableFileInput(forms.widgets.ClearableFileInput):
    template_name = 'app/forms/widgets/clearable_file_input.html'


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
                static('dist/ext/flatpickr/themes/primary.css'),
            )
        }
        js = (
            static('dist/ext/flatpickr/flatpickr.js'),
            static('dist/js/datepicker.js'),
        )
