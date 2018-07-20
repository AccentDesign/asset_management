from django.db import models

from assets.middleware.current_user import get_current_user


class TaskHistory(models.Model):
    task = models.ForeignKey(
        'assets.Task',
        on_delete=models.CASCADE,
        related_name='history'
    )
    notes = models.TextField(
        blank=True
    )
    status = models.ForeignKey(
        'assets.TaskStatus',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        editable=False,
        default=get_current_user
    )
    date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'task history'
