from django import forms

from assets.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'address': forms.widgets.Textarea(attrs={'rows': 6})
        }
