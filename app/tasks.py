from django.core.management import call_command

from huey import crontab
from huey.contrib.djhuey import db_periodic_task


@db_periodic_task(crontab(hour='1', minute='0'))
def reset_all_scheduled_task_due_dates():
    call_command('updateschedules')
