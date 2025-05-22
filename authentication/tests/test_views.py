from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            is_staff=True
        )
    
    def test_login_success(self):
        """Test successful login"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh(self):
        """Test token refresh"""
        # First login to get tokens
        login_url = reverse('token_obtain_pair')
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(login_url, login_data)
        refresh_token = login_response.data['refresh']
        
        # Test refresh
        refresh_url = reverse('token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_verify_token(self):
        """Test token verification"""
        self.client.force_authenticate(user=self.user)
        url = reverse('verify_token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        self.assertEqual(response.data['user']['username'], 'testuser')
    
    def test_user_registration_requires_staff(self):
        """Test that only staff can register new users"""
        # Create non-staff user
        non_staff_user = User.objects.create_user(
            username='regular',
            password='test123'
        )
        self.client.force_authenticate(user=non_staff_user)
        
        url = reverse('user_register')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'email': 'new@example.com'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_profile_retrieval(self):
        """Test user profile retrieval"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
