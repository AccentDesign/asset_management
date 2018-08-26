from django.urls import reverse

from tests.test_case import AppTestCase


class TestListView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.url = '{}?q=root+asset'.format(reverse('assets:search'))
        self.url_no_query = reverse('assets:search')

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next=/search/%3Fq%3Droot%2Basset'.format(reverse('login'))
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

    def test_each_team_only_sees_their_results(self):
        self.client.force_login(self.team1.members.first())
        assert self.team1_asset
        context = self.client.get(self.url).context
        self.assertEqual(context[-1]['count'], 1)
        self.assertEqual(context[-1]['object_list'][0], self.team1_asset)

        self.client.force_login(self.team2.members.first())
        assert self.team2_asset
        context = self.client.get(self.url).context
        self.assertEqual(context[-1]['count'], 1)
        self.assertEqual(context[-1]['object_list'][0], self.team2_asset)

    def test_no_query_returns_empty_list(self):
        self.client.force_login(self.team1.members.first())
        assert self.team1_asset
        context = self.client.get(self.url_no_query).context
        self.assertEqual(context[-1]['count'], 0)
        self.assertEqual(context[-1]['object_list'], [])

        self.client.force_login(self.team2.members.first())
        assert self.team2_asset
        context = self.client.get(self.url_no_query).context
        self.assertEqual(context[-1]['count'], 0)
        self.assertEqual(context[-1]['object_list'], [])
