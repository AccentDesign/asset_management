from django import forms

from images.models import Image
from images.validators import validate_image_file_extension

from app.forms.widgets import ClearableFileInput
from authentication.models import User


class MyProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        validators=[validate_image_file_extension],
        widget=ClearableFileInput()
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'avatar'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.picture:
            self.fields['avatar'].initial = self.instance.picture.file

    def save(self, commit=False):
        instance = super().save(commit)
        avatar = self.cleaned_data.get('avatar')

        if not avatar:
            # if there is an image delete it
            if instance.picture:
                instance.picture.delete()
            instance.picture = None
        else:
            # either change the existing image or add a new one
            if instance.picture:
                instance.picture.file = avatar
                instance.picture.title = avatar.name
                instance.picture.save()
            else:
                image = Image.objects.create(
                    file=avatar,
                    title=avatar.name
                )
                instance.picture = image

        return super().save(commit=True)
