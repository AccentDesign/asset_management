from rest_framework import generics, viewsets

from assets.models import Status
from assets.serializers import StatusSerializer


class StatusViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Status.objects
    serializer_class = StatusSerializer
