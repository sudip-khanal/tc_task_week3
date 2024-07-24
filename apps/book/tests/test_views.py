from django.db.models import Avg

from rest_framework import status

from apps.book.models import  Book,Favorite
from apps.review.models import Review
from apps.book.serializers import BookSerializer,FavoriteBookSerializer
from apps.review.serializer import ReviewSerializer
from apps.book.tests.factories import BookFactory,FavoriteFactory
from apps.review.tests.factories import ReviewFactory
from rest_framework.test import APIClient
from config.test import TestApi
from apps.user.tests.factories import UserFactory
from rest_framework.test import force_authenticate

class TestBookViews(TestApi):
      
    # def auth_client(self, create_user):
    #     client = APIClient()
    #     client.force_authenticate(user=create_user)
    #     return client   
    
    def test_create_book(self):
        user = self.create_user()
        self.client.force_authenticate(user=user)  # Authenticate the user
        url = '/book/'
        data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'description': 'Book description',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      
        self.assertEqual(response.data['title'], data['title'])

        created_by_username = response.data['created_by']['username']
        created_by_email=response.data['created_by']['email']
        
        self.assertEqual(created_by_username, user.username)
        self.assertEqual(created_by_email,user.email)


    def test_update_book(self):
        user = self.create_user()
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'description': 'Updated Description',
            'is_active': True
        }
        self.client.force_authenticate(user=user) 
        response = self.client.put(url, data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload the book from the database
        book.refresh_from_db()
        
        # Check the updated fields
        self.assertEqual(book.title, data['title'])
        # Check the updated_by field
        self.assertEqual(book.created_by, user)

    def test_update_book_by_another_user(self):
        self.user=self.create_user()
        print(self.user)
        book = BookFactory(created_by=self.user)
        another_user = self.create_user()
        print(another_user)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'description': 'Updated Description',
            'is_active': True
        }
        self.client.force_authenticate(user=another_user) 
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_partial_update_book(self):
        user = self.create_user()
        print(user)
        book = BookFactory(created_by=user)
        print(book)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Partially Updated Title'
        }
        self.client.force_authenticate(user=user) 
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Reload the book from the database
        book.refresh_from_db()
        # Check the updated field
        self.assertEqual(book.title, data['title'])
        print(book.created_by)
        # Check the updated_by field
        self.assertEqual(book.created_by, user)

    
    def test_partial_update_by_another_user(self):
        user = self.create_user()
        print(user)
        book = BookFactory(created_by=user)
        another_user=self.create_user()
        print(another_user)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Partially Updated Title'
        }
        self.client.force_authenticate(user=another_user) 
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_destroy_book(self):
        user = self.create_user()
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'
        self.client.force_authenticate(user=user) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
         # Reload the book from the database
        book.refresh_from_db()
        
        # Check that the book is not active
        self.assertFalse(book.is_active)

    def test_destroy_book_by_another_user(self):
        user = self.create_useruser()
        book = BookFactory(created_by=user)
        another_user = self.create_user()
        url = f'/book/{book.id}/'
        self.client.force_authenticate(user=another_user) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_favorite_book(self):
        user=self.create_user()
        print(user)
        book = BookFactory()
        url=f'/book/{book.id}/favorite/'
        client = self.auth_client(user)
        response=client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_by_username = response.data['user']['username']
        print(created_by_username)
        self.assertEqual(created_by_username,user.username)
        self.assertEqual(response.data['book'],book.id)

    def test_favorite_others_book(self):
        user=self.create_user()
        book = BookFactory(created_by=user)
        another_user=self.create_user()
        self.client.force_authenticate(user=another_user)
        

    
    def test_favorite_book_unauthorized_user(self):
        user = self.create_user()
        book = BookFactory()
        url = f'/book/{book.id}/favorite/'
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_unfavorite_book(self):
        user=self.create_user
        book = BookFactory(created_by=user)
        favorite = FavoriteFactory (user=user, book=book)
        url = f'/book/{book.id}/unfavorite/'
        client = self.auth_client(user)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



    def test_top_rated_books(self):
        url = 'http://localhost:8000/book/top-10-rated/'
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])


    def test_my_favorites(self):
        favorites = FavoriteFactory.create_batch(3,user=self.user)
        url = 'book/my_favorites/'
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        serializer = FavoriteBookSerializer(favorites, many=True)
        assert response.data == serializer.data
        # test filters

    def test_retrieve_book_with_reviews(self):
        book = BookFactory.create(created_by=self.user)
        reviews = ReviewFactory.create_batch(3, book=book)
        
        url = f'http://127.0.0.1:8000/book/{book.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check the book data
        self.assertEqual(response.data['title'], book.title)
        self.assertEqual(response.data['author'], book.author)
        self.assertEqual(response.data['description'], book.description)
        # Check the reviews
        reviews_data = response.data['reviews']
        review_serializer = ReviewSerializer(reviews, many=True)
        self.assertEqual(reviews_data, review_serializer.data)
        # Check the average rating
        reviews_queryset = Review.objects.filter(book=book)
        average_rating = reviews_queryset.aggregate(avg_rating=Avg('rating'))['avg_rating']
        self.assertEqual(response.data['average_rating'], average_rating)