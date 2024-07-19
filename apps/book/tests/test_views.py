from django.test import Client, TestCase
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from apps.book.models import Book
from apps.book.serializers import BookSerializer

class TestBookViewSet(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.auth_headers = {'HTTP_AUTHORIZATION': 'Token ' + self.token.key} 
        self.book1 = Book.objects.create(title="Book 1", author="Author 1", description="Description 1", is_active=True, created_by=self.user)
        self.book2 = Book.objects.create(title="Book 2", author="Author 2", description="Description 2", is_active=True, created_by=self.user)
        self.book3 = Book.objects.create(title="Book 3", author="Author 3", description="Description 3", is_active=False, created_by=self.user)

    def test_list_books(self):
        url = 'http://127.0.0.1:8000/book/'
        response = self.client.get(url)
        books = Book.objects.filter(is_active=True)
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_book(self):
        url = f'http://127.0.0.1:8000/book/{self.book2.id}/'
        response = self.client.get(url)
        serializer = BookSerializer(self.book1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        url = 'http://127.0.0.1:8000/book/'
        data = {
        'title': 'Book 4',
        'author': 'Author 4',
        'description': 'Description 4',
        'created_by': self.user.id,
        'is_active': True
        }
        response = self.client.post(url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)



    def test_update_book(self):
        url = f'http://127.0.0.1:8000/book/{self.book1.id}/'  
        data = {
            'title': 'Updated Book 1',
            'author': 'Updated Author 1',
            'description': 'Updated Description 1',
            'is_active': True,
            'created_by': self.user.id
        }
        response = self.client.put(url, data, content_type='application/json', **self.auth_headers)
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, data['title'])
        self.assertEqual(self.book1.author, data['author'])
        self.assertEqual(self.book1.description, data['description'])

    def test_partial_update(self):
        url = f'http://127.0.0.1:8000/book/{self.book1.id}/'
        data = {
            'title': 'Updated Book 3',
            'description': 'Updated Description 3',
        }
        response = self.client.patch(url, data, content_type='application/json', **self.auth_headers)
        self.book1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, data['title'])
        self.assertEqual(self.book1.description, data['description'])


    def test_delete_book(self):
        url = f'http://127.0.0.1:8000/book/{self.book2.id}/'
        response = self.client.delete(url, **self.auth_headers)
        self.book2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.book2.is_active)

    def test_create_favourite(self):
        url=f'http://localhost:8000/book/{self.book2.id}/favorite/'
       
        response = self.client.post(url,**self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_my_favourite():
        pass
    def test_unfavourite():
        pass

    def test_top_books():
        pass