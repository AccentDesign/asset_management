from rest_framework import generics, viewsets

from assets.models import Task
from assets.serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSetMixin, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Task.objects
    serializer_class = TaskSerializer
