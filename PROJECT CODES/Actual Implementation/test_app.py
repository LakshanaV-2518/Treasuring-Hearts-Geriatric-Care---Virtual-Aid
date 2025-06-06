import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_registration(self):
        # Test successful registration
        response = self.app.post('/register', data={'username1': 'testuser', 'password1': 'testpassword', 'email': 'test@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Username or email already exists', response.data)

    def test_login(self):
        # Test successful login with both username and password
        tester = app.test_client(self)
        response = tester.post('/login_form', data={'username': 'testuser', 'password': 'testpassword'})

        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["status"], "success")

        # Test login with incorrect username
        response = tester.post('/login_form', data={'username': 'wronguser', 'password': 'wrongpassword'})
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["status"], "error")
        self.assertIn("Login failed", response_json["message"])


if __name__ == '__main__':
    unittest.main()