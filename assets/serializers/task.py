from rest_framework import serializers

from assets.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'task_type',
            'asset',
            'assigned_to',
            'task_priority',
            'due_date'
        )
