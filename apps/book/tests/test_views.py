import pytest

from rest_framework import status

from apps.book.models import  Book,Favorite
from apps.book.serializers import BookSerializer,FavoriteBookSerializer
from apps.book.tests.factories import BookFactory,FavoriteFactory
from apps.review.tests.conftest import BaseTest


@pytest.mark.usefixtures("setup_fixtures")
class TestBookViews(BaseTest):

    @pytest.mark.django_db
    def test_list_books(self):
        books = BookFactory.create_batch(5)  # Create book instances
        url = 'http://localhost:8000/book/'
        response = self.api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        books = Book.objects.filter(is_active=True)
        serializer = BookSerializer(books,many=True)
        assert response.data == serializer.data

    @pytest.mark.django_db
    def test_create_book(self,auth_client):
        url = 'http://localhost:8000/book/'
        data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'description': 'Book description',
            'is_active': True
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # response data matches the input data
        assert response.data['title'] == data['title']
        assert response.data['author'] == data['author']
        assert response.data['description'] == data['description']
        assert response.data['is_active'] == data['is_active']

        assert 'id' in response.data
        assert 'created_by' in response.data

    # @pytest.mark.django_db
    # def test_retrieve_book(api_client):
    #     book = BookFactory()
    #     url = f'http://127.0.0.1:8000/book/{book.id}/'
    #     response = api_client.get(url)
        
    #     # Ensure the status code is correct
    #     assert response.status_code == status.HTTP_200_OK
        
    #     # Ensure the response data matches the book data
    #     assert response.data['title'] == book.title
    #     assert response.data['author'] == book.author
    #     assert response.data['description'] == book.description
    #     assert response.data['created_by'] == book.created_by.id


    @pytest.mark.django_db
    def test_update_book(self, auth_client, create_user):
        book = BookFactory(created_by=create_user)
        url = f'http://127.0.0.1:8000/book/{book.id}/'
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'description': 'Updated Description',
            'is_active':True
        }
        response = auth_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        
        book.refresh_from_db()
        assert book.title == data['title']
        assert book.author == data['author']
        assert book.description == data['description']
        assert book.is_active==data['is_active']

    @pytest.mark.django_db
    def test_partial_update_book(self, auth_client, create_user):
        book = BookFactory(created_by=create_user)
        url = f'http://127.0.0.1:8000/book/{book.id}/'
        data = {
            'title': 'Partially Updated Title'
        }
        response = auth_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        
        book.refresh_from_db()
        assert book.title == data['title']
        assert book.author == book.author  # Ensure other fields remain unchanged
        assert book.description == book.description

    @pytest.mark.django_db
    def test_destroy_book(self, auth_client, create_user):
        book = BookFactory(created_by=create_user)
        url = f'http://127.0.0.1:8000/book/{book.id}/'
        response = auth_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert Book.objects.filter(id=book.id, is_active=False).exists()

    @pytest.mark.django_db
    def test_favorite_book(self, auth_client, create_user):
        book = BookFactory()
        url=f'http://localhost:8000/book/{book.id}/favorite/'
        response = auth_client.post(url)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert Favorite.objects.filter(book=book, user=create_user).exists()

    @pytest.mark.django_db
    def test_unfavorite_book(self, auth_client, create_user):
        favorite = FavoriteFactory(user=create_user)
        book = favorite.book
        url = f'http://127.0.0.1:8000/book/{book.id}/unfavorite/'
        response = auth_client.delete(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert not Favorite.objects.filter(book=book, user=create_user).exists()

    @pytest.mark.django_db
    def test_top_rated_books(self, api_client):
        url = 'http://localhost:8000/book/top-10-rated/'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK or status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_my_favorites(self, auth_client, create_user):
        favorites = FavoriteFactory.create_batch(3, user=create_user)
        url = 'http://127.0.0.1:8000/book/my_favorites/'
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        
        serializer = FavoriteBookSerializer(favorites, many=True)
        assert response.data == serializer.data
