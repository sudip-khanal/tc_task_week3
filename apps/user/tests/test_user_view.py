from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.contrib.auth.tokens import default_token_generator
from config.test import TestApi
from apps.user.tests.factories import UserFactory
from rest_framework.test import APIClient

class TestUser(TestApi):

      
    def auth_client(self, create_user):
        client = APIClient()
        client.force_authenticate(user=create_user)
        return client
    
    def test_change_password(self):
        self.user = self.create_user()
        client = self.auth_client(create_user=self.user) 
        
        url = '/user/change_password/'  # Update this to match your URL pattern
        data = {
            'old_password': 'password@123',  # Ensure the old password matches what was set
            'new_password': 'newpassword@123',
            'confirm_new_password': 'newpassword@123'
        }
        
        response = client.post(url, data)  # Use the authenticated client
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        user = self.create_user()  # This sets the password to 'password@123'
        url = '/user/login/'  # Ensure the trailing slash if needed
        data = {
            'username': user.username,
            'password': 'password@123'  # This should match the password set in create_user
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        # Ensure the response contains the token
        self.assertIsNotNone(response.data['token'])

    def test_register_user(self):
        url = '/user/register/'
        data = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password': 'password@123',
            'confirm_password': 'password@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'],data['username'])
        self.assertEqual(response.data['email'],data['email'])

    def test_logout(self):
        self.user = self.create_user()
        client = self.auth_client(create_user=self.user)  # Authenticate the client and get the user
        # Perform the logout operation
        url ='/user/logout/'  # Ensure this matches your logout URL pattern
        response = client.post(url)
        # Verify the response status code
        self.assertEqual(response.status_code, 200)


    def test_verify_email(self):
        user = UserFactory(is_active=False)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('verify_email',args=[uidb64,token])#params
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        user.refresh_from_db()#mail response make mock
        self.assertTrue(user.is_active)


  # use moking and params 

    def test_forgot_password(self):
        url = reverse('forgot_password')
        data = {
            'email': self.user.email
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200) # mock mail


    def test_reset_password(self):
        user = self.create_user() # 
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('reset_password', args=[uid, token])#params
        data = {
            'new_password': 'password@1234',
            'confirm_new_password': 'password@1234'
        }
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, 200)













