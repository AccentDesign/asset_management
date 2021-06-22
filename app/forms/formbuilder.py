from collections import OrderedDict

from django import forms
from django.utils.module_loading import import_string

from app.forms import widgets


class BaseField:
    field_class = forms.Field
    name = "Field"
    widgets = [forms.widgets.TextInput]

    @classmethod
    def attrs(cls):
        return {
            'label': '',
            'widget': None,
            'required': False,
            'initial': None,
            'help_text': None,
        }

    @classmethod
    def options(cls):
        return {
            'name': cls.name,
            'attrs': cls.attrs(),
            'widgets': [{
                "type": ".".join([w.__module__, w.__name__]),
                "name": str(w.__name__),
            } for w in cls.widgets]
        }

    def field(self, attrs):
        base_attrs = self.attrs()
        base_attrs.update(attrs)
        return self.field_class(**base_attrs)


class BooleanField(BaseField):
    field_class = forms.BooleanField
    name = "BooleanField"
    widgets = [forms.widgets.CheckboxInput]


class CharField(BaseField):
    field_class = forms.CharField
    name = "CharField"
    widgets = [forms.widgets.TextInput, forms.widgets.Textarea]


class ChoiceField(BaseField):
    field_class = forms.ChoiceField
    name = "ChoiceField"
    widgets = [forms.widgets.Select, widgets.RadioSelect]

    @classmethod
    def attrs(cls):
        attrs = super().attrs()
        attrs.update({'choices': []})
        return attrs


class DateField(BaseField):
    field_class = forms.DateField
    name = "DateField"
    widgets = [widgets.DatePicker]


class DecimalField(BaseField):
    field_class = forms.DecimalField
    name = "DecimalField"
    widgets = [forms.widgets.NumberInput]

    @classmethod
    def attrs(cls):
        attrs = super().attrs()
        attrs.update({
            'max_digits': None,
            'decimal_places': None,
        })
        return attrs


class EmailField(BaseField):
    field_class = forms.EmailField
    name = "EmailField"
    widgets = [forms.widgets.EmailInput]


class GenericIPAddressField(BaseField):
    field_class = forms.GenericIPAddressField
    name = "GenericIPAddressField"
    widgets = [forms.widgets.TextInput]


class IntegerField(BaseField):
    field_class = forms.IntegerField
    name = "IntegerField"
    widgets = [forms.widgets.NumberInput]


class MultipleChoiceField(BaseField):
    field_class = forms.MultipleChoiceField
    name = "MultipleChoiceField"
    widgets = [widgets.CheckboxSelectMultiple, forms.widgets.SelectMultiple]

    @classmethod
    def attrs(cls):
        attrs = super().attrs()
        attrs.update({'choices': []})
        return attrs


class TimeField(BaseField):
    field_class = forms.TimeField
    name = "TimeField"
    widgets = [forms.widgets.TimeInput]


class URLField(BaseField):
    field_class = forms.URLField
    name = "URLField"
    widgets = [forms.widgets.URLInput]


class FormBuilderBaseForm(forms.Form):
    pass


class FormBuilder:
    field_classes = [
        BooleanField,
        CharField,
        ChoiceField,
        DateField,
        DecimalField,
        EmailField,
        GenericIPAddressField,
        IntegerField,
        MultipleChoiceField,
        TimeField,
        URLField,
    ]

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

            # get the base props for the field and update them
            # from the field data, NOT adding new keys
            props = field_cls.attrs()
            props.update((k, field[k]) for k in set(field).intersection(props))

            # if a widget was specified use it
            if props['widget']:
                props['widget'] = import_string(props['widget'])

            # if there are choices and its a select add a blank option
            if 'choices' in props:
                if issubclass(props['widget'], forms.widgets.Select):
                    props['choices'].insert(0, (None, '---------'))

            # add the field to the form
            formfields[key] = field_cls().field(props)

        return formfields

    @classmethod
    def field_meta_data(cls):
        return {
            ".".join([f.__module__, f.__name__]): f.options()
            for f in cls.field_classes
        }

    def get_form_class(self):
        return type(str("AppFormBuilder"), (FormBuilderBaseForm,), self.formfields)
