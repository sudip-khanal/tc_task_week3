import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from apps.user.tests.factories import UserFactory 

class BaseTest:
    @pytest.fixture(autouse=True)
    def setup_fixtures(self, api_client, create_user, auth_client):
        self.api_client = api_client
        self.create_user = create_user
        self.auth_client = auth_client

    @staticmethod
    @pytest.fixture
    def api_client():
        return APIClient()

    @staticmethod
    @pytest.fixture
    def create_user():
        user = UserFactory()
        user.set_password('password123')
        user.save()
        return user

    @staticmethod
    @pytest.fixture
    def auth_client(create_user):
        client = APIClient()
        client.force_authenticate(user=create_user)
        return client
