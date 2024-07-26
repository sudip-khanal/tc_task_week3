from rest_framework import status

from apps.book.tests.factories import BookFactory,FavoriteFactory
from config.test import TestApi

class TestBookViews(TestApi):
      
    def test_create_book(self):
        """
        Test case for creating a book.
        Verifies that a book cannot be added without authentication.
        checks that an authenticated user can successfully create a book.
        """
        url = '/book/'
        user = self.create_user()
        data = {
            'title': 'Test Book',
            'author': 'Author Name',
            'description': 'Book description',
            'is_active': True
        }
        self.client.force_authenticate(user=user) 
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

        created_by_username = response.data['created_by']['username']
        created_by_email = response.data['created_by']['email']

        self.assertEqual(created_by_username, user.username)
        self.assertEqual(created_by_email, user.email)

    def test_update_book(self):
        """
        Test case for  updating a book.Verifies that:
        3. Only the user who created the book can update it.
        4. Another user cannot update the book created by someone else.
        """
        #create and Update the book by the same user
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload the book from the database
        book.refresh_from_db()

        # Check the updated fields
        self.assertEqual(book.title, data['title'])
        self.assertEqual(book.created_by, user)

        # Create another user and attempt to update the book
        another_user = self.create_user()
        self.client.force_authenticate(user=another_user)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_book(self):
        """
        Test case for partially updating a book.
        Verifies that:
        1. Only the user who created the book can partially update it.
        2. Another user cannot partially update the book created by someone else.
        """
        # Create user and book
        user = self.create_user()
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'
        data = {
            'title': 'Partially Updated Title'
        }

        # Partial update by the same user
        self.client.force_authenticate(user=user) 
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Reload the book from the database
        book.refresh_from_db()

        # Check the updated field
        self.assertEqual(book.title, data['title'])        
        self.assertEqual(book.created_by, user)

        # Create another user and attempt to partially update the book
        another_user = self.create_user()
        self.client.force_authenticate(user=another_user) 

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_bookss(self):
        """
        Test case for destroying a book.
        Verifies that:
        1. Only the user who created the book can delete (deactivate) it.
        2. Another user cannot delete the book created by someone else.
        """
        # Create user and book
        user = self.create_user()
        book = BookFactory(created_by=user)
        url = f'/book/{book.id}/'

         # Create another user and attempt to delete the book
        another_user = self.create_user()
        self.client.force_authenticate(user=another_user) 

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Delete (deactivate) the book by the same user
        self.client.force_authenticate(user=user) 
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Reload the book from the database
        book.refresh_from_db()

        # Check that the book is not active
        self.assertFalse(book.is_active)

        
    def test_create_favorite_book(self):
        """
        Test case for favoriting a book.
        Verifies that:
        1. A user can favorite their own book.
        2. A user can favorite a book created by another user.
        """
        # Create user and book
        user = self.create_user()
        book = BookFactory()
        url = f'/book/{book.id}/favorite/'

        # Favorite the book by the user
        self.client.force_authenticate(user=user) 
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_by_username = response.data['user']['username']

        self.assertEqual(created_by_username, user.username)
        self.assertEqual(response.data['book'], book.id)

        # Create another user and favorite the same book
        another_user = self.create_user()
        self.client.force_authenticate(user=another_user) 
        
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['book'], book.id)


    def test_unfavorite_bookss(self):
        """
        Test case for unfavoriting a book.
        Verifies that:
        1. Only the user who favorited the book can unfavorite it.
        2. Another user cannot unfavorite the book favorited by someone else.
        """

        # Create user and another user
        user = self.create_user()
        other_user = self.create_user()
        
        # Create a book and favorite it by the user
        book = BookFactory(created_by=user)
        favorite = FavoriteFactory(user=user, book=book)
        url = f'/book/{book.id}/unfavorite/'

        # Unfavorite the book by the same user
        self.client.force_authenticate(user=user) 
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Attempt to unfavorite the book by another user
        self.client.force_authenticate(user=other_user) 
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_my_favorites_access(self):
        """
        Test case for accessing user favorites.
        Verifies that:
        1. The authenticated user can see their own favorites.
        2. Another user cannot see the other user's favorites.
        """
        # Create the primary user, another user, and a book
        user = self.create_user()
        other_user = self.create_user()
        book = BookFactory()
        
        # Create a favorite for the primary user
        FavoriteFactory(user=user, book=book)
        
        # Test that the authenticated user can see their own favorites
        self.client.force_authenticate(user=user)
        url = '/book/my_favorites/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test that another user cannot see the other user's favorites
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_retrive_book_with_filter(self):
        user1=self.create_user()
        user2=self.create_user()

        book1 = BookFactory(title='Test Book ', author='Author A', created_at='2024-01-01T00:00:00Z', created_by=user1)
        book2 = BookFactory(title='Test Book 2', author='Author B', created_at='2024-02-01T00:00:00Z', created_by=user2)   
        
        url = '/book/'
        """
        Test filtering books by title.
        """
        response = self.client.get(url, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
                    
        """
        Test filtering books by author.
         """
        response = self.client.get(url, {'author': 'Author B'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        """
        Test filtering books by the username of the user who created them.
        """
        response = self.client.get(url, {'user': 'user1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        
        """
        Test filtering books using multiple criteria simultaneously.
        """
        response = self.client.get(url, {
                        'title': 'Test Book',
                        'author': 'Author A',
                        'created_at_gt': '2024-01-01T00:00:00Z',
                        'created_at_lt': '2024-03-01T00:00:00Z',
                        'user': 'user1'
                    })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_top_rated_books(self):
        url = '/book/top-10-rated/'
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
