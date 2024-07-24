from rest_framework import status

from apps.book.tests.factories import BookFactory, UserFactory
from apps.review.models import Review
from apps.review.serializer import ReviewSerializer
from apps.review.tests.factories import ReviewFactory
from config.test import TestApi
from rest_framework.test import APIClient


class TestReviewViews(TestApi):

       
    # def auth_client(self, create_user):
    #     client = APIClient()
    #     client.force_authenticate(user=create_user)
    #     return client

    def test_create_review(self):
        book = BookFactory() 
        user = self.create_user()  # Use the create_user method to create the user
        
        # Authenticate the user
        self.client.force_login(user=user)
        
        url = '/review/'  # Update this to match your URL pattern
        data = {
            'book': book.id,
            'user': user.id,
            'rating': 4,
            'review_text': 'Great book!'
        }
        
        response = self.client.post(url, data)  # Use the authenticated client
        assert response.status_code == status.HTTP_201_CREATED
