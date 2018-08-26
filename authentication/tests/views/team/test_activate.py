from django.urls import reverse

from tests.test_case import AppTestCase


class TestActivateView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.user = self.create_user()
        self.team1.members.add(self.user)
        self.url = reverse('team-activate', kwargs={'pk': self.team1.pk})

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_can_activate(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        # sets the active team
        self.user.refresh_from_db()
        self.assertEqual(self.user.activated_team, self.team1)

        # redirects to home
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_cannot_activate_a_team_when_not_a_member(self):
        self.client.force_login(self.user)
        url = reverse('team-activate', kwargs={'pk': self.team2.pk})
        response = self.client.get(url)

        # does not set the active team
        self.user.refresh_from_db()
        self.assertIsNone(self.user.activated_team)

        # redirects to home
        self.assertRedirects(response, reverse('home'), 302, 200)
