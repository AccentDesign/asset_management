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
        on_delete=models.CASCADE
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

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def schedule(self):
        """ returns the rrule for the duration of the tasks scheduling """

        if self.repeat_interval is not None and self.repeat_frequency is not None:
            return rrule(
                freq=self.repeat_frequency,
                dtstart=self.initial_due_date,
                interval=self.repeat_interval,
                until=self.repeat_until,
            )

        return None

    @property
    def last_due(self):
        """ Returns the datetime the task was last due on """

        if self.schedule:
            return self.schedule.before(datetime.now())

        if self.initial_due_date and self.initial_due_date <= datetime.now().date():
            return datetime(
                self.initial_due_date.year,
                self.initial_due_date.month,
                self.initial_due_date.day
            )

    @property
    def next_due(self):
        """ Returns the datetime the task is next due on """

        if self.schedule:
            return self.schedule.after(datetime.now())

        if self.initial_due_date and self.initial_due_date > datetime.now().date():
            return datetime(
                self.initial_due_date.year,
                self.initial_due_date.month,
                self.initial_due_date.day
            )
