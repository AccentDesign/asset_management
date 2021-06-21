from django.urls import reverse

from assets.models import Task
from tests.test_case import AppTestCase


class TestUpdateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.object = self.collection1_task
        self.url = reverse('assets:task-update', kwargs={'pk': self.object.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_user_with_no_active_collection_redirects_home(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_login_grants_access(self):
        self.client.force_login(self.collection1.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_404_when_object_is_for_another_collection(self):
        self.client.force_login(self.collection2.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_can_update_task(self):
        self.client.force_login(self.collection1.members.first())
        post_data = {
            'name': 'some edited name',
            'task_type': self.object.task_type_id,
            'initial_due_date': self.object.initial_due_date.strftime('%Y-%m-%d'),
            'assigned_to': self.object.assigned_to_id
        }
        response = self.client.post(self.url, post_data)

        # was updated
        Task.objects.get(
            pk=self.object.pk,
            name=post_data['name'],
            task_type_id=post_data['task_type'],
            initial_due_date=self.object.initial_due_date,
            assigned_to_id=post_data['assigned_to']
        )

        # successful post always redirects to detail url
        self.assertRedirects(response, self.object.get_absolute_url(), 302, 200)

    def test_empty_post_stays_on_url(self):
        self.client.force_login(self.collection1.members.first())
        post_data = {}
        response = self.client.post(self.url, post_data)

        # doesnt go anywhere
        self.assertEqual(response.status_code, 200)
