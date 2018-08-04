from django import forms

from images.models import Image

from authentication.models import User


class MyProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'profile_picture'
        )

    def save(self, commit=True):
        instance = super().save(commit)
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            image = Image.objects.create(title=instance.get_full_name(), file=picture)
            instance.picture = image
            instance.save()
        return instance
