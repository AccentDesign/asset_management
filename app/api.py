from rest_framework import generics, viewsets
from rest_framework.response import Response

from images.exceptions import InvalidFilterSpecError
from images.models import Image
from images.shortcuts import get_rendition_or_not_found

from .serializers import ImageRenditionSerializer


class ImageRenditionViewSet(viewsets.ViewSetMixin, generics.RetrieveAPIView):
    """ API readonly endpoint for image. """

    queryset = Image.objects.all()
    serializer_class = ImageRenditionSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Return an image rendition instance.

        Optionally pass:

            ?filter_spec=width-500 to get a 500 wide
            ?filter_spec=height-500 to get a 500 high
            ?filter_spec=height-500|format-jpeg to get a 500 high jpeg
            omit to get the original version

        If you pass an invalid filter_spec you will be sent the original version of the image.
        """

        instance = self.get_object()
        filter_spec = self.request.query_params.get('filter_spec', 'original')

        try:
            rendition = get_rendition_or_not_found(instance, filter_spec)
        except InvalidFilterSpecError:
            rendition = get_rendition_or_not_found(instance, 'original')

        serializer = self.get_serializer(rendition)

        return Response(serializer.data)
