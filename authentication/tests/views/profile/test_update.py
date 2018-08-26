from django.urls import reverse

from tests.test_case import AppTestCase


class TestProfileView(AppTestCase):

    def setUp(self):
        self.user = self.create_user()
        self.url = reverse('my_profile')

    def test_login_required(self):
        response = self.client.get(self.url)
        expected_url = '{}?next={}'.format(reverse('login'), self.url)
        self.assertRedirects(response, expected_url, 302, 200)

    def test_login_grants_access(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_can_update(self):
        self.client.force_login(self.user)
        post_data = {
            'email': 'someemail@example.com',
            'first_name': 'Some',
            'last_name': 'User',
            'avatar': self.get_temporary_image(),
            'focal_point_x': 50,
            'focal_point_y': 50,
            'focal_point_width': 100,
            'focal_point_height': 100
        }

        response = self.client.post(self.url, post_data, format='multipart')

        # was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, post_data['email'])
        self.assertEqual(self.user.first_name, post_data['first_name'])
        self.assertEqual(self.user.last_name, post_data['last_name'])
        self.assertIsNotNone(self.user.picture)
        self.assertEqual(self.user.picture.focal_point_x, post_data['focal_point_x'])
        self.assertEqual(self.user.picture.focal_point_y, post_data['focal_point_y'])
        self.assertEqual(self.user.picture.focal_point_width, post_data['focal_point_width'])
        self.assertEqual(self.user.picture.focal_point_height, post_data['focal_point_height'])

        # edit always redirects to profile url
        self.assertRedirects(response, self.url, 302, 200)
