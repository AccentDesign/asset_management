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
    focal_point_x = forms.IntegerField(widget=forms.widgets.HiddenInput, required=False)
    focal_point_y = forms.IntegerField(widget=forms.widgets.HiddenInput, required=False)
    focal_point_width = forms.IntegerField(widget=forms.widgets.HiddenInput, required=False)
    focal_point_height = forms.IntegerField(widget=forms.widgets.HiddenInput, required=False)

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'avatar',
            'focal_point_x',
            'focal_point_y',
            'focal_point_width',
            'focal_point_height'
        )

    class Media:
        css = {
            'all': (
                'images/css/Jcrop.min.css',
                'images/css/focal-point-chooser.css'
            )
        }
        js = (
            'images/js/jquery.ba-throttle-debounce.min.js',
            'images/js/Jcrop.min.js',
            'images/js/focal-point-chooser.js',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.picture:
            self.fields['avatar'].initial = self.instance.picture.file
            self.fields['focal_point_x'].initial = self.instance.picture.focal_point_x
            self.fields['focal_point_y'].initial = self.instance.picture.focal_point_y
            self.fields['focal_point_width'].initial = self.instance.picture.focal_point_width
            self.fields['focal_point_height'].initial = self.instance.picture.focal_point_height

    def save(self, commit=False):
        instance = super().save(commit)

        avatar = self.cleaned_data.get('avatar')
        focal_point_x = self.cleaned_data.get('focal_point_x')
        focal_point_y = self.cleaned_data.get('focal_point_y')
        focal_point_width = self.cleaned_data.get('focal_point_width')
        focal_point_height = self.cleaned_data.get('focal_point_height')

        if not avatar:
            # if there is an image delete it
            if instance.picture:
                instance.picture.delete()
            instance.picture = None

        else:
            # either change the existing image
            if instance.picture:
                instance.picture.file = avatar
                instance.picture.title = avatar.name
                instance.picture.focal_point_x = focal_point_x
                instance.picture.focal_point_y = focal_point_y
                instance.picture.focal_point_width = focal_point_width
                instance.picture.focal_point_height = focal_point_height
                instance.picture.save()

            # or add a new one
            else:
                image = Image.objects.create(
                    file=avatar,
                    title=avatar.name,
                    focal_point_x=focal_point_x,
                    focal_point_y=focal_point_y,
                    focal_point_width=focal_point_width,
                    focal_point_height=focal_point_height
                )
                instance.picture = image

        return super().save(commit=True)
