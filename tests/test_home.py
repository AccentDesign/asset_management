from tests.test_case import AppTestCase


class ViewTests(AppTestCase):

    def test_200_response(self):
        user = self.create_user()
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
