from rest_framework import generics, viewsets

from assets.models import TaskStatus
from assets.serializers import TaskStatusSerializer


class TaskStatusViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = TaskStatus.objects
    serializer_class = TaskStatusSerializer
