from datetime import datetime, timedelta

from dateutil.rrule import DAILY
from mock import mock

from app.tasks import reset_all_scheduled_task_due_dates
from tests.test_case import AppTestCase


class TestCommand(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.task = self.team1_task
        self.task.initial_due_date = datetime.today().date()
        self.task.repeat_interval = 1
        self.task.repeat_frequency = DAILY
        self.task.save()

    def test_reset_all_scheduled_task_due_dates(self):
        reset_all_scheduled_task_due_dates()

        self.team1_task.refresh_from_db()
        self.assertEqual(self.team1_task.due_date, datetime.today().date())

        with mock.patch('assets.models.task.datetime') as mocked:
            mocked.now.return_value = datetime.now() + timedelta(days=1)

            reset_all_scheduled_task_due_dates()

            self.team1_task.refresh_from_db()
            self.assertEqual(self.team1_task.due_date, datetime.today().date() + timedelta(days=1))

        with mock.patch('assets.models.task.datetime') as mocked:
            mocked.now.return_value = datetime.now() + timedelta(days=100)

            reset_all_scheduled_task_due_dates()

            self.team1_task.refresh_from_db()
            self.assertEqual(self.team1_task.due_date, datetime.today().date() + timedelta(days=100))
