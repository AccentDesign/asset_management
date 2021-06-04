from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management import call_command
from django.db import models
from django.template.defaultfilters import pluralize

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, task

from assets.models import Task
from authentication.models import Team


@task(retries=3, retry_delay=60)
def send_email(subject, body, to, reply_to):
    """ Send an email. """
    email = EmailMessage(subject=subject, body=body, to=to, reply_to=reply_to)
    email.send()


@db_periodic_task(crontab(hour='1', minute='0'))
def reset_all_scheduled_task_due_dates():
    """ Run the update schedules command. """
    call_command('updateschedules')


@db_periodic_task(crontab(hour='7', minute='0'))
def send_daily_reminders():
    """ Email all members of each team if they have tasks due. """

    today = datetime.today().date()

    for team in Team.objects.all():
        to_addresses = [member.email for member in team.members.all()]
        subject = 'Asset Management - Daily Task Reminder - {}'.format(team)

        task_count = Task.objects.filter(due_date__lte=today, asset__team=team).count()

        if task_count > 0:

            intro = (
                'As of today there are a total of {} task{} due. '
                'Below is a breakdown of who these tasks are assigned to:\n'.format(task_count, pluralize(task_count))
            )

            content = [intro, ]

            assigned_tasks = (
                Task.objects
                .filter(due_date__lte=today, asset__team=team, assigned_to__isnull=False)
                .values('assigned_to__first_name', 'assigned_to__email')
                .annotate(total=models.Count('assigned_to'))
                .order_by('assigned_to')
            )

            if len(assigned_tasks) > 0:
                for row in assigned_tasks:
                    content.append(
                        '- {} ({}) has {} task{} due'.format(
                            row['assigned_to__first_name'],
                            row['assigned_to__email'],
                            row['total'],
                            pluralize(row['total'])
                        )
                    )

            else:
                content.append('- No tasks have been assigned to any team members')

            content.append('\n')
            content.append('Thanks.')
            content.append(settings.APPLICATION_URL)

            content = '\n'.join(content)

            send_email(subject, content, to_addresses, None)
