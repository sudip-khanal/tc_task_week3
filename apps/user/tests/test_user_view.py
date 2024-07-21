import pytest
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('register')  
    data = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password': 'password@123',
            'confirm_password': 'password@123'
        }
    response = api_client.post(url, data)
    print(response.data) 
    assert response.status_code == 201
    assert response.data['msg'] == "Register successfully. Check your email for verification."

@pytest.mark.django_db
def test_verify_email(api_client, create_user):
    user = create_user
    user.is_active = False
    user.save()
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = reverse('verify_email', args=[uidb64, token])  
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['msg'] == 'Email verified successfully.'
    user.refresh_from_db()
    assert user.is_active

@pytest.mark.django_db
def test_user_login(api_client, create_user):
    url = reverse('login')  
    data = {
            'username': create_user.username,
            'password': 'password@123'
        }
    response = api_client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_change_password(auth_client):
    url = reverse('change_password')  
    data = {
            'old_password': 'password@123',
            'new_password': 'password@321',
            'confirm_new_password':'password@321' 
        }
    response = auth_client.post(url, data)
    print(response.data) 
    assert response.status_code == 200
    assert response.data['msg'] == 'Password changed successfully.'

@pytest.mark.django_db
def test_forgot_password(api_client, create_user):
    url = reverse('forgot_password')  
    data = {
            'email': create_user.email
        }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data['msg'] == 'Password reset email sent successfully.'

@pytest.mark.django_db
def test_reset_password(api_client, create_user):
    user = create_user
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    url = reverse('reset_password', args=[uid, token])
    data = {
            'new_password': 'password@1234',
            'confirm_new_password': 'password@1234'
        }
    response = api_client.post(url, data)
    print(response.data) 
    assert response.status_code == 200
    assert response.data['msg'] == 'Password reset successfully.'

@pytest.mark.django_db
def test_logout(auth_client):
    url = reverse('logout')  
    response = auth_client.post(url)
    assert response.status_code == 200
    assert response.data['msg'] == 'Logged out successfully.'
















