from rest_framework import generics, viewsets

from assets.models import Asset
from assets.serializers import AssetSerializer


class AssetViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Asset.objects
    serializer_class = AssetSerializer
