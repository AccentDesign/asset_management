from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from tests.test_case import AppTestCase


class TestDeleteView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        assert self.collection1_task
        self.object = self.collection1
        self.url = reverse('collection-delete', kwargs={'pk': self.object.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_login_grants_access_for_admin(self):
        self.client.force_login(self.collection1.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_non_admin_cannot_access(self):
        user = self.create_user()
        self.collection1.members.add(user)
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_can_delete(self):
        self.client.force_login(self.collection1.admin)
        post_data = {}
        response = self.client.post(self.url, post_data)

        # was deleted
        with self.assertRaises(ObjectDoesNotExist):
            self.object.refresh_from_db()

        # redirects to root nodes url when no parent
        self.assertRedirects(response, reverse('home'), 302, 200)
