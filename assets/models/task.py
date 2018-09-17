import uuid
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.timezone import make_naive

from dateutil.rrule import (
    rrule,
    DAILY,
    MONTHLY,
    WEEKLY,
    YEARLY
)

from authentication.middleware.current_user import get_current_team


class TaskManager(models.Manager):
    def get_queryset(self):
        """ Returns the base queryset with additional properties """

        qs = super().get_queryset().annotate(
            qs_last_completed=models.Max(
                'history__date',
                filter=models.Q(history__status__name='Completed')
            )
        )

        team = get_current_team()

        if team:
            qs = qs.filter(asset__team=team)

        return qs

    def search(self, query=None):
        """ Returns the search results for the main site search """

        qs = self.get_queryset()
        if query:
            all_filters = models.Q()
            for term in query.split():
                or_lookup = (
                    models.Q(name__icontains=term) |
                    models.Q(description__icontains=term) |
                    models.Q(asset__name__icontains=term) |
                    models.Q(asset__description__icontains=term) |
                    models.Q(task_type__name__icontains=term) |
                    models.Q(assigned_to__first_name__icontains=term) |
                    models.Q(assigned_to__last_name__icontains=term)
                )
                all_filters = all_filters & or_lookup
            qs = qs.filter(all_filters).distinct()
        return qs

    def due_by_date(self, date=None, assigned_to=None):
        """
        Returns tasks sorted by due_date that are due up to and including the date parameter.
        Optionally filters by the assigned to user
        """

        if not date:
            date = datetime.today().date()

        filters = {'due_date__lte': date}

        if assigned_to:
            filters['assigned_to'] = assigned_to

        return (
            self.get_queryset()
            .filter(**filters)
            .select_related(
                'asset',
                'assigned_to',
                'task_priority'
            )
            .order_by(
                'due_date'
            )
        )


class Task(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
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
    assigned_to = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    task_priority = models.ForeignKey(
        'assets.TaskPriority',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    initial_due_date = models.DateField()
    repeat_interval = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )
    repeat_frequency = models.IntegerField(
        choices=(
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

    # managed via model signals
    due_date = models.DateField(
        null=True,
        editable=False
    )

    for_team = TaskManager()
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('assets:task-update', kwargs={'pk': self.pk})

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
            dtstart=self.initial_due_date,
            interval=self.repeat_interval,
            until=self.repeat_until,
        )

    @property
    def schedule_text(self):
        """ returns a friendly string describing the schedule """

        if self.repeat_interval is None or self.repeat_frequency is None:
            return None

        return 'Every {} {}'.format(
            self.repeat_interval,
            self.get_repeat_frequency_display()
        )

    @property
    def last_due(self):
        """ Returns the date the task was last due on """

        if self.schedule:
            due = self.schedule.before(self.now)
            return due.date() if due else None

        if self.initial_due_date and self.initial_due_date <= self.now.date():
            return self.initial_due_date

    @property
    def next_due(self):
        """ Returns the date the task is next due on """

        if self.schedule:
            due = self.schedule.after(self.now)
            return due.date() if due else None

        if self.initial_due_date and self.initial_due_date > self.now.date():
            return self.initial_due_date

    @property
    def last_completed(self):
        """
        Returns the last completed date from TaskManager.get_queryset
        falls back to running the query inline
        """

        if hasattr(self, 'qs_last_completed'):
            return getattr(self, 'qs_last_completed')

        try:
            return self.history.filter(status__name='Completed').latest('date').date
        except ObjectDoesNotExist:
            return None

    def get_current_schedule_dates(self):
        """ calculate the current due date of the task """

        due_date = None
        last_completed = self.last_completed

        if self.last_due and not last_completed:
            due_date = self.last_due
        elif self.last_due and last_completed and self.last_due > make_naive(last_completed).date():
            due_date = self.last_due
        elif self.next_due:
            due_date = self.next_due

        return due_date, last_completed


@receiver(pre_save, sender=Task)
def pre_save_task(instance, **kwargs):
    """ On pre save of a task update its schedule """

    due_date, last_completed = instance.get_current_schedule_dates()
    instance.due_date = due_date
