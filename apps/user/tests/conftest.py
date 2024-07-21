import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.user.tests.factories import UserFactory 

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    user = UserFactory()
    user.set_password('password@123')
    user.save()
    return user

@pytest.fixture
def auth_client(create_user):
    client = APIClient()
    token, created = Token.objects.get_or_create(user=create_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client

