from django.urls import reverse

from authentication.models import Collection
from tests.test_case import AppTestCase


class TestCreateView(AppTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.url = reverse('collection-create')

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_login_grants_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_can_create(self):
        self.client.force_login(self.user)
        post_data = {
            'title': 'some title'
        }
        response = self.client.post(self.url, post_data)

        # was created and admin set
        collection = Collection.objects.get(
            title=post_data['title'],
            admin=self.user,
            members=self.user
        )

        # redirects to activate url
        self.assertRedirects(response, reverse('collection-activate', kwargs={'pk': collection.pk}), 302, 302)
