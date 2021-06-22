# Generated by Django 3.2.4 on 2021-06-22 14:11
from django.db import migrations
from app.forms.formbuilder import FormBuilder

from assets.models import AssetType


def migrate_fields(apps, schema_editor):
    mapping = {
        'django.forms.BooleanField': 'app.forms.formbuilder.BooleanField',
        'django.forms.CharField': 'app.forms.formbuilder.CharField',
        'django.forms.ChoiceField': 'app.forms.formbuilder.ChoiceField',
        'django.forms.DateField': 'app.forms.formbuilder.DateField',
        'django.forms.DecimalField': 'app.forms.formbuilder.DecimalField',
        'django.forms.EmailField': 'app.forms.formbuilder.EmailField',
        'django.forms.GenericIPAddressField': 'app.forms.formbuilder.GenericIPAddressField',
        'django.forms.IntegerField': 'app.forms.formbuilder.IntegerField',
        'django.forms.MultipleChoiceField': 'app.forms.formbuilder.MultipleChoiceField',
        'django.forms.TimeField': 'app.forms.formbuilder.TimeField',
        'django.forms.URLField': 'app.forms.formbuilder.URLField',
    }
    for asset in AssetType.objects.all():
        for key, value in asset.fields.items():
            asset.fields[key]['type'] = mapping[value['type']]
        asset.save()
        assert FormBuilder(asset.fields).get_form_class() is not None


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0007_auto_20210618_2248'),
    ]

    operations = [
        migrations.RunPython(migrate_fields)
    ]