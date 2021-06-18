from datetime import datetime, timedelta

from dateutil.rrule import DAILY
from django.core.management import call_command
from mock import mock

from tests.test_case import AppTestCase


class TestCommand(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.task = self.collection1_task
        self.task.initial_due_date = datetime.today().date()
        self.task.repeat_interval = 1
        self.task.repeat_frequency = DAILY
        self.task.save()

    def test_due_date_set_correctly_when_days_change(self):
        call_command('updateschedules')

        self.collection1_task.refresh_from_db()
        self.assertEqual(self.collection1_task.due_date, datetime.today().date())

        with mock.patch('assets.models.task.datetime') as mocked:
            mocked.now.return_value = datetime.now() + timedelta(days=1)

            call_command('updateschedules')

            self.collection1_task.refresh_from_db()
            self.assertEqual(self.collection1_task.due_date, datetime.today().date() + timedelta(days=1))

        with mock.patch('assets.models.task.datetime') as mocked:
            mocked.now.return_value = datetime.now() + timedelta(days=100)

            call_command('updateschedules')

            self.collection1_task.refresh_from_db()
            self.assertEqual(self.collection1_task.due_date, datetime.today().date() + timedelta(days=100))
