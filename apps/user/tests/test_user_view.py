from unittest.mock import patch

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status

from config.test import TestApi
from apps.user.tests.factories import UserFactory


class TestUser(TestApi):
    @patch('apps.user.tasks.send_verification_email_task')
    def test_register_user(self, mock_send_verification_email_task):
        """
        Test case for user registration.
        Verifies that:
        1. A new user can be successfully registered with valid data.
        2. The response contains the correct username and email.
        3. Registration fails if the username or email is already taken.
        """
        url = '/user/register/'

        # Data for registering a new user
        data = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password': 'password@123',
            'confirm_password': 'password@123'
        }

        # Register the new user
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_id = response.data['id']
        self.assertTrue(mock_send_verification_email_task(user_id).is_callled())

    def test_verify_email(self):
        # Create a user who is not yet active
        user = UserFactory(is_active=False)

        # Generate the URL parameters
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = f'/user/verify_email/{uidb64}/{token}/'  
        
        # Simulate the user clicking the verification link
        response = self.client.get(url)
        # Check the response status
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        user.refresh_from_db()
        # Check that the user is now active
        self.assertTrue(user.is_active)

    def test_user_login(self):
        """
        Test case for user login.
        Verifies that:
        A user can successfully log in with valid credentials.
        Login fails with invalid credentials.
        """
        user = self.create_user() 
        url = '/user/login/' 
        # Data for a valid login attempt
        data = {
            'username': user.username,
            'password': 'password@123'  
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure the response contains the token
        self.assertIsNotNone(response.data['token'])

    def test_change_passwords(self):
        """
        Test case for changing a user's password.
        Verifies that:
        1. A user can successfully change their password with valid data.
        2. The new password confirmation matches the new password.
        """
        user = self.create_user()
        self.client.force_authenticate(user=user)

        url = '/user/change_password/' 

        # Test changing password with incorrect old password
        old_pass_wrong_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newpassword@123',
            'confirm_new_password': 'newpassword@123'
        }
        response = self.client.post(url, old_pass_wrong_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)

        # Valid data for changing the password
        data = {
            'old_password': 'password@123',  
            'new_password': 'newpassword@123',
            'confirm_new_password': 'newpassword@123'
        }
        # Change the password
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_logout(self):
        """
        Test case for user logout.
        Verifies that:
        1. An authenticated user can successfully log out.
        2. The logout operation invalidates the user's token.
        """
        # Create and authenticate the user
        user = self.create_user()
        self.client.force_authenticate(user=user) 
        
        url = '/user/logout/' 
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Attempt to access a protected endpoint with the same after the logout
        protected_url = '/user/change_password/' 
        protected_response = self.client.get(protected_url)
        
        # Verify that access to the protected endpoint is denied
        self.assertEqual(protected_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch('apps.user.tasks.send_reset_email_task')  
    def test_forgot_password_send_mail(self, mock_send_reset_email_task):
        """
        Test case for forgot password functionality.
        Verifies that:
        1. A password reset email is sent when a valid email is provided.
        2. The response contains the correct message.
        3. The email sending task is called with the correct user ID.
        """
        # Create a user with an email
        user = UserFactory(email='testuser@example.com')

        url = '/user/forgot_password/'  
        data = {
            'email': 'testuser@example.com'
        }
        
        response = self.client.post(url, data)
        self.assertTrue(mock_send_reset_email_task.is_callled())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
     
    def test_reset_passwords(self):
        """
        Test case for resetting a user's password 
        Verifies that:
        1. The password reset process works with a valid UID and token.
        3. The user can log in with the new password.
        """
        # This user should have received a reset password  link in email
        user = self.create_user()  

        # # Generate UID and token for password reset 
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = f'/user/reset_password/{uid}/{token}/'

        # Data for resetting the password
        data = {
            'new_password': 'password@1234',
            'confirm_new_password': 'password@1234'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

         # Test with an invalid token
        invalid_token_url = f'/user/reset_password/{uid}/invalidtoken/'
        response = self.client.post(invalid_token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
        # Attempt to log in with the new password
        login_data = {
            'username': user.username,
            'password': 'password@1234'
        }
        response = self.client.post('/user/login/', login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

