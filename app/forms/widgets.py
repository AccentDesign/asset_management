import json

from django import forms
from django.templatetags.static import static


class CheckboxInput(forms.widgets.CheckboxInput):
    def __init__(self, attrs={}, choices=()):
        attrs['class'] = 'checkbox'
        super().__init__(attrs)


class CheckboxSelectMultiple(forms.widgets.CheckboxSelectMultiple):
    def __init__(self, attrs={}, choices=()):
        attrs['class'] = 'checkboxes'
        super().__init__(attrs)


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

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js',
        )

    def get_context(self, name, value, attrs):
        from app.forms.formbuilder import FormBuilder

        context = super().get_context(name, value, attrs)
        context.update({
            'field_meta_data': json.dumps(FormBuilder.field_meta_data()),
            'field_ids': json.dumps([
                k for k, _
                in sorted(json.loads(value).items(), key=lambda i: i[1].get('order', 0))
            ])
        })
        return context


class RadioSelect(forms.widgets.RadioSelect):
    def __init__(self, attrs={}, choices=()):
        attrs['class'] = 'radios'
        super().__init__(attrs)
