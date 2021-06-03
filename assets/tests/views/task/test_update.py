from django.urls import reverse

from assets.models import Task, TaskHistory
from tests.test_case import AppTestCase


class TestUpdateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.object = self.team1_task
        self.url = self.object.get_absolute_url()

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_user_with_no_active_team_redirects_home(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_login_grants_access(self):
        self.client.force_login(self.team1.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_404_when_object_is_for_another_team(self):
        self.client.force_login(self.team2.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_can_update_task(self):
        self.client.force_login(self.team1.members.first())
        post_data = {
            'task_update': '',
            'task_form-name': 'some edited name',
            'task_form-task_type': self.object.task_type_id,
            'task_form-initial_due_date': self.object.initial_due_date.strftime('%d/%m/%Y'),
            'task_form-assigned_to': self.object.assigned_to_id
        }
        response = self.client.post(self.url, post_data)

        # was updated
        Task.objects.get(
            pk=self.object.pk,
            name=post_data['task_form-name'],
            task_type_id=post_data['task_form-task_type'],
            initial_due_date=self.object.initial_due_date,
            assigned_to_id=post_data['task_form-assigned_to']
        )

        # successful post always redirects to node url
        self.assertRedirects(response, self.object.asset.get_nodes_url(), 302, 200)

    def test_can_add_task_history_notes(self):
        self.client.force_login(self.team1.members.first())
        post_data = {
            'history_notes': '',
            'history_form-notes': 'some notes',
            'history_form-task': self.object.pk
        }
        response = self.client.post(self.url, post_data)

        # was updated
        TaskHistory.objects.get(
            task_id=self.object.pk,
            notes=post_data['history_form-notes'],
            status_id=None
        )

        # successful post always redirects to node url
        self.assertRedirects(response, self.object.asset.get_nodes_url(), 302, 200)

    def test_can_complete_task(self):
        self.client.force_login(self.team1.members.first())
        post_data = {
            'history_complete': '',
            'history_form-notes': 'some notes',
            'history_form-task': self.object.pk
        }
        response = self.client.post(self.url, post_data)

        # was updated
        TaskHistory.objects.get(
            task_id=self.object.pk,
            notes=post_data['history_form-notes'],
            status__name='Completed'
        )

        # successful post always redirects to edit url
        self.assertRedirects(response, self.object.asset.get_nodes_url(), 302, 200)

    def test_empty_post_stays_on_url(self):
        self.client.force_login(self.team1.members.first())
        post_data = {}
        response = self.client.post(self.url, post_data)

        # doesnt go anywhere
        self.assertEqual(response.status_code, 200)
