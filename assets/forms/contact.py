from django import forms
from django.utils.safestring import mark_safe

from assets.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'address': forms.widgets.Textarea(attrs={'rows': 6})
        }

    def __init__(self, *args, **wkargs):
        super().__init__(*args, **wkargs)
        if self.instance.address:
            self.fields['address'].help_text = mark_safe(
                "Search for address on {}.".format(self.instance.google_maps_link)
            )
