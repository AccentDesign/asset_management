from rest_framework import generics, viewsets

from assets.models import TaskPriority
from assets.serializers import TaskPrioritySerializer


class TaskPriorityViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = TaskPriority.objects
    serializer_class = TaskPrioritySerializer
