from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

ME_URL = reverse('users_app:me')

CREATE_USER_URL = reverse('users_app:create')
TOKEN_URL = reverse('users_app:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test users API(public)"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': "tests5@test.com",
            'password': 'testpass123',
            'name': 'TestName'
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Tests creating user that already exist will fail"""
        create_user(**self.payload)

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password(self):
        """Test pasword now just for too short"""
        self.payload['password'] = '123'

        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=self.payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test if a token is created for the user"""
        create_user(**self.payload)
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(**self.payload)
        self.payload['password'] = 'wrongPassword'

        res = self.client.post(TOKEN_URL, self.payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload_emp = self.payload
        payload_emp['password'] = ''
        res = self.client.post(TOKEN_URL, payload_emp)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # payload_emp = payload
        # payload_emp['email'] = ''
        # res = self.client.post(TOKEN_URL, payload_emp)

        # self.assertNotIn('token', res.data)
        # self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test that authentication is required for suers"""
        res = self.client.get(ME_URL)

        self.assertTrue(res.status_code == status.HTTP_401_UNAUTHORIZED
                        or res.status_code == status.HTTP_403_FORBIDDEN)


class PrivateUserApiTests(TestCase):
    """Test API requests that require auth"""

    def setUp(self):
        self.user = create_user(
            email="tests5@test.com",
            password='testpass5',
            name='TestName5',
        )
        self.client = APIClient()
        # Auth dummy user in apiclient for tests
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """"Test that post is not allowed on 'me' url"""

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_prfile(self):
        """Test updating the user profile for auth user"""
        # new updated data
        payload = {
            'email': "tests6@test.com",
            'password': 'tes5523',
            'name': 'NewUser'
        }

        res = self.client.patch(ME_URL, payload)

        # update user with lates values from database
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
