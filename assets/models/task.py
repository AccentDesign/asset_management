from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models

from dateutil.rrule import (
    rrule,
    DAILY,
    HOURLY,
    MONTHLY,
    WEEKLY,
    YEARLY
)


class TaskManager(models.Manager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        return super().get_queryset().annotate(
            qs_last_completed=models.Max('completions__date')
        )


class Task(models.Model):
    name = models.CharField(
        max_length=255
    )
    description = models.TextField(
        blank=True
    )
    task_type = models.ForeignKey(
        'assets.TaskType',
        on_delete=models.PROTECT
    )
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    initial_due_date = models.DateField()
    repeat_interval = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    repeat_frequency = models.IntegerField(
        choices=(
            (HOURLY, 'Hour(s)'),
            (DAILY, 'Day(s)'),
            (WEEKLY, 'Week(s)'),
            (MONTHLY, 'Month(s)'),
            (YEARLY, 'Year(s)'),
        ),
        null=True,
        blank=True
    )
    repeat_until = models.DateField(
        null=True,
        blank=True
    )

    objects = TaskManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def initial_due_datetime(self):
        """ returns the initial due date as a datetime"""

        if not self.initial_due_date:
            return None

        return datetime(
            self.initial_due_date.year,
            self.initial_due_date.month,
            self.initial_due_date.day
        )

    @property
    def repeat_until_datetime(self):
        """ returns the repeat until date as a datetime"""

        if not self.repeat_until:
            return None

        return datetime(
            self.repeat_until.year,
            self.repeat_until.month,
            self.repeat_until.day
        )

    @property
    def now(self):
        """ returns now """

        return datetime.now()

    @property
    def schedule(self):
        """ returns the rrule for the duration of the tasks scheduling """

        if self.repeat_interval is None or self.repeat_frequency is None:
            return None

        return rrule(
            freq=self.repeat_frequency,
            dtstart=self.initial_due_datetime,
            interval=self.repeat_interval,
            until=self.repeat_until_datetime,
        )

    @property
    def last_due(self):
        """ Returns the datetime the task was last due on """

        if self.schedule:
            return self.schedule.before(self.now)

        if self.initial_due_datetime and self.initial_due_datetime <= self.now:
            return self.initial_due_datetime

    @property
    def next_due(self):
        """ Returns the datetime the task is next due on """

        if self.schedule:
            return self.schedule.after(self.now)

        if self.initial_due_datetime and self.initial_due_datetime > self.now:
            return self.initial_due_datetime

    @property
    def last_completed(self):
        """ Returns the last completed date from TaskManager.get_queryset """

        return getattr(self, 'qs_last_completed', None)
