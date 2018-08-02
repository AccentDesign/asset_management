from rest_framework import serializers

from assets.models import TaskStatus


class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = (
            'id',
            'name'
        )
