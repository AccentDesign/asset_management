from django.urls import reverse

from tests.test_case import AppTestCase


class TestListView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.url = reverse('assets:file-list')

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

    def test_each_team_only_sees_their_object_list(self):
        assert self.team1_file
        self.client.force_login(self.team1.members.first())
        context = self.client.get(self.url).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.team1.file_set.first())

        assert self.team2_file
        self.client.force_login(self.team2.members.first())
        context = self.client.get(self.url).context
        self.assertEqual(context[-1]['object_list'].count(), 1)
        self.assertEqual(context[-1]['object_list'].first(), self.team2.file_set.first())