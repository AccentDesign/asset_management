from rest_framework import generics, viewsets

from assets.models import TaskType
from assets.serializers import TaskTypeSerializer


class TaskTypeViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = TaskType.objects
    serializer_class = TaskTypeSerializer
