from rest_framework import serializers

from assets.models import TaskType


class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = (
            'id',
            'name'
        )
