from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

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


@receiver(post_save, sender=TaskHistory)
@receiver(post_delete, sender=TaskHistory)
def post_task_history(instance, **kwargs):
    """ On save and delete of a task history """

    def set_task_schedule():
        # we just need to save the task as they are set in the pre_save
        # catch in case the history is being deleted due to the task being deleted
        try:
            instance.task.save()
        except ObjectDoesNotExist:
            pass

    transaction.on_commit(set_task_schedule)
