"""
Tests for user api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test public feature of the user api."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user is successful"""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if assword less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # verify didn't create an object
        is_user_exist = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
        self.assertFalse(is_user_exist, "User obj shouldn't be created")

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_password(self):
        """Test returns error if credentials are invalid."""
        create_user(email='test@example.com', password='testpass123')

        payload = {'email': 'test@example.com', 'password': 'invalidpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_invalid_email(self):
        """Test returns error if credentials are invalid."""
        create_user(email='test@example.com', password='testpass123')

        payload = {'email': 'test2@example.com', 'password': 'testpass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_empty_password(self):
        """Test returns error if credentials are invalid."""
        create_user(email='test@example.com', password='testpass123')

        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
 """Test private feature of the user api that require authentication"""
 def setUp(self):
     self.user = create_user(
         email='test@example.com',
         password='testpass123',
         name='Test Name',
     )
     self.client = APIClient()
     self.client.force_login(user=self.user)

def test_retrieve_profile_success(self):
    """Test retrieving profile for logged in user."""
    res = self.client.get(ME_URL)

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(res.data, {
        'email': self.user.email,
        'name': self.user.name,
    })

def test_me_not_allowed(self):
    """Test POST is not allowed for me endpoint"""
    res = self.client.post(ME_URL, {})

    self.assertEquals(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

def test_update_user_profile(self):
    """Test updating user profile for logged in user."""
    payload = {
        'name': 'updated_name',
        'password': 'newtestpass123',
    }
    res = self.client.patch(ME_URL, payload)

    self.user.refresh_from_db()
    self.assertEqual(self.user.name, payload['name'])
    self.assertTrue(self.user.check_password(payload['password']))
    self.assertEqual(res.status_code, status.HTTP_200_OK)
