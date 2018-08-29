from django.urls import reverse

from assets.models import Note, File
from tests.test_case import AppTestCase


class TestUploadView(AppTestCase):
    fixtures = ['tests/fixtures/test.yaml']

    def setUp(self):
        self.url = reverse('assets:file-upload')

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_user_with_no_active_team_redirects_home(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('home'), 302, 200)

    def test_login_grants_access_but_no_get(self):
        self.client.force_login(self.team1.members.first())
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_can_upload(self):
        self.client.force_login(self.team1.members.first())
        post_data = {
            'file': self.get_temporary_image()
        }
        response = self.client.post(self.url, post_data, format='multipart')

        # was created for correct team
        file = File.objects.filter(team=self.team1).latest('uploaded_by')

        # ensure correct response
        response_dict = {
            'name': str(file),
            'url': file.file.url,
            'size': file.file.size
        }

        self.assertJSONEqual(response.content, response_dict)
