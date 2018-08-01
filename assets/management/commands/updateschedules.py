from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from assets.models import Task


class Command(BaseCommand):
    help = 'Updates the task schedule for all tasks.'

    def get_queryset(self):
        return Task.objects.exclude(
            Q(repeat_interval__isnull=True) |
            Q(repeat_frequency__isnull=True)
        )

    def handle(self, *args, **options):
        queryset = self.get_queryset()

        count = queryset.count()

        with transaction.atomic():
            for task in queryset:
                task.save()

        msg = 'Successfully updated the schedules for %s tasks' % count
        self.stdout.write(self.style.SUCCESS(msg))
