from rest_framework import serializers

from images.models import Rendition


class ImageRenditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rendition
        fields = (
            'id',
            'image',
            'file',
            'width',
            'height',
            'filter_spec'
        )
