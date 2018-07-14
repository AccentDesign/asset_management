from django.db import models


class TaskCompletion(models.Model):
    task = models.ForeignKey(
        'assets.Task',
        on_delete=models.CASCADE,
        related_name='completions'
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['date']
