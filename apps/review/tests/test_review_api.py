import pytest
from rest_framework import status

from apps.book.tests.factories import BookFactory, UserFactory
from apps.review.models import Review
from apps.review.serializer import ReviewSerializer
from apps.review.tests.factories import ReviewFactory
from apps.review.tests.conftest import BaseTest

@pytest.mark.usefixtures("setup_fixtures")
class TestReviewViews(BaseTest):

    @pytest.mark.django_db
    def test_list_reviews(self, auth_client):
        # Create a few review instances
        reviews = ReviewFactory.create_batch(5)  # Create review instances
        url = 'http://localhost:8000/review/'
        response = auth_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK

        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        assert response.data == serializer.data

    @pytest.mark.django_db
    def test_create_review(self, auth_client):
        book = BookFactory()
        user = UserFactory()
        
        url = 'http://localhost:8000/review/'  
        data = {
            'book': book.id,
            'user': user.id,
            'rating': 4,
            'review_text': 'Great book!'
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        
   
