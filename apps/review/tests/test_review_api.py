from rest_framework import status

from apps.book.tests.factories import BookFactory
from apps.review.tests.factories import ReviewFactory
from config.test import TestApi


class TestReviewViews(TestApi):
  
    def test_create_review(self):
        """
        Test case for creating a review for a book.
        Verifies that:
        1. A review can be successfully created with valid data.
        """
        book = BookFactory()
        
        review = ReviewFactory(book=book)

        user = self.create_user()  
        self.client.force_authenticate(user=user)  #

        url = '/review/'  
        data = {
            'book': book.id,  
            'user': user.id,  
            'rating': 4,  
            'review_text': 'Great book!'  
        }
        response = self.client.post(url, data)        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
