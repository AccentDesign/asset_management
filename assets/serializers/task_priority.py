from rest_framework import serializers

from assets.models import TaskPriority


class TaskPrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskPriority
        fields = (
            'id',
            'name'
        )
