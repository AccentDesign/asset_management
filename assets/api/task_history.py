from rest_framework import viewsets

from assets.models import TaskHistory
from assets.serializers import TaskHistorySerializer


class TaskHistoryViewSet(viewsets.ModelViewSet):
    queryset = TaskHistory.objects
    serializer_class = TaskHistorySerializer
