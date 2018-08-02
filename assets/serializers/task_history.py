from rest_framework import serializers

from assets.models import TaskHistory


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = (
            'id',
            'task',
            'notes',
            'status',
            'user',
            'date'
        )
