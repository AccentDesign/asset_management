from collections import OrderedDict

from django import forms
from django.utils.module_loading import import_string


class FormBuilderBaseForm(forms.Form):
    pass


class FormBuilder:
    def __init__(self, fields):
        self.fields = fields

    @property
    def formfields(self):
        """ Return a list of form fields from the registered fields. """

        formfields = OrderedDict()

        # add each field to the form
        for key, field in sorted(self.fields.items(), key=lambda i: i[1].get('order', 0)):

            # import the field class
            field_cls = import_string(field['type'])

            # copy the props
            props = {
                'label': field['label'],
                'widget': field['widget'],
                'required': field['required'],
                'initial': field['initial'],
                'help_text': field['help_text'],
            }

            # prepare each field attr
            if 'initial' in props:
                if props['initial'] is None or props['initial'] == '':
                    del props['initial']

            if 'label' in props:
                if props['label'] is None or props['label'] == '':
                    del props['label']

            if 'widget' in props:
                if props['widget']:
                    props['widget'] = import_string(props['widget'])
                else:
                    del props['widget']

            if issubclass(field_cls, forms.ChoiceField):
                if len(field['choices']) > 0:
                    props['choices'] = [(c, c) for c in field['choices']]
                else:
                    props['choices'] = []
                if issubclass(props['widget'], forms.widgets.Select):
                    props['choices'].insert(0, (None, '---------'))

            if issubclass(field_cls, forms.DecimalField):
                props['max_digits'] = field.get('max_digits', 0)
                props['decimal_places'] = field.get('decimal_places', 0)

            # add the field to the form
            formfields[key] = field_cls(**props)

        return formfields

    @classmethod
    def field_data_template(cls):
        return {
            'label': '',
            'type': '',
            'widget': '',
            'initial': '',
            'help_text': '',
            'required': False,
            'order': 0,
            'choices': [],
            'decimal_places': None,
            'max_digits': None
        }

    @classmethod
    def field_meta_data(cls):
        return {
            'django.forms.BooleanField': {
                'name': 'BooleanField',
                'widgets': [
                    {
                        'type': 'app.forms.widgets.CheckboxInput',
                        'name': 'CheckboxInput'
                    },
                ]
            },
            'django.forms.CharField': {
                'name': 'CharField',
                'widgets': [
                    {
                        'type': 'django.forms.widgets.TextInput',
                        'name': 'TextInput'
                    },
                    {
                        'type': 'django.forms.widgets.Textarea',
                        'name': 'Textarea'
                    },
                ]
            },
            'django.forms.ChoiceField': {
                'name': 'ChoiceField',
                'has_choices': True,
                'widgets': [
                    {
                        'type': 'django.forms.widgets.Select',
                        'name': 'Select'
                    },
                    {
                        'type': 'app.forms.widgets.RadioSelect',
                        'name': 'RadioSelect'
                    },
                ]
            },
            'django.forms.DateField': {
                'name': 'DateField',
                'widgets': [
                    {
                        'type': 'app.forms.widgets.DatePicker',
                        'name': 'DatePicker'
                    },
                ]
            },
            'django.forms.DecimalField': {
                'name': 'DecimalField',
                'has_max_digits': True,
                'has_decimal_places': True,
                'widgets': [
                    {
                        'type': 'django.forms.widgets.NumberInput',
                        'name': 'NumberInput'
                    },
                ]
            },
            'django.forms.EmailField': {
                'name': 'EmailField',
                'widgets': [
                    {
                        'type': 'django.forms.widgets.EmailInput',
                        'name': 'EmailInput'
                    },
                ]
            },
            'django.forms.GenericIPAddressField': {
                'name': 'GenericIPAddressField',
                'widgets': [
                    {
                        'type': 'django.forms.widgets.TextInput',
                        'name': 'TextInput'
                    },
                ]
            },
            'django.forms.IntegerField': {
                'name': 'IntegerField',
                'widgets': [
                    {
                        'type': 'django.forms.widgets.NumberInput',
                        'name': 'NumberInput'
                    },
                ]
            },
            'django.forms.MultipleChoiceField': {
                'name': 'MultipleChoiceField',
                'has_choices': True,
                'widgets': [
                    {
                        'type': 'app.forms.widgets.CheckboxSelectMultiple',
                        'name': 'CheckboxSelectMultiple'
                    },
                    {
                        'type': 'django.forms.widgets.SelectMultiple',
                        'name': 'SelectMultiple'
                    },
                ]
            },
            'django.forms.TimeField': {
                'name': 'TimeField',
                'widgets': [
                    {
                        'type': 'django.forms.widgets.TimeInput',
                        'name': 'TimeInput'
                    },
                ]
            },
            'django.forms.URLField': {
                'name': 'URLField',
                'widgets': [
                    {
                        'type': 'django.forms.widgets.URLInput',
                        'name': 'URLInput'
                    },
                ]
            },
        }

    def get_form_class(self):
        return type(str("AppFormBuilder"), (FormBuilderBaseForm,), self.formfields)
