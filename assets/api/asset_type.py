from rest_framework import generics, viewsets

from assets.models import AssetType
from assets.serializers import AssetTypeSerializer


class AssetTypeViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = AssetType.objects
    serializer_class = AssetTypeSerializer
