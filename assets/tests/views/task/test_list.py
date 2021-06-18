from datetime import datetime

from django.urls import reverse

from tests.test_case import AppTestCase


class TestListView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.url = reverse('assets:task-list')
        self.filtered_url = '{}?due_date={}'.format(
            self.url,
            datetime.today().date().strftime('%Y-%m-%d')
        )
        self.filtered_url_invalid = '{}?due_date=foo'.format(self.url)

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

    def test_each_collection_only_sees_their_object_list(self):
        self.client.force_login(self.collection1.members.first())
        assert self.collection1_task
        context = self.client.get(self.url).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.collection1_task)

        self.client.force_login(self.collection2.members.first())
        assert self.collection2_task
        context = self.client.get(self.url).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.collection2_task)

    def test_filtered_object_list(self):
        self.client.force_login(self.collection1.members.first())
        assert self.collection1_task
        context = self.client.get(self.filtered_url).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.collection1_task)

        self.client.force_login(self.collection2.members.first())
        assert self.collection2_task
        context = self.client.get(self.filtered_url).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.collection2_task)

    def test_invalid_filter_is_ignored(self):
        self.client.force_login(self.collection1.members.first())
        assert self.collection1_task
        context = self.client.get(self.filtered_url_invalid).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.collection1_task)

        self.client.force_login(self.collection2.members.first())
        assert self.collection2_task
        context = self.client.get(self.filtered_url_invalid).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.collection2_task)
