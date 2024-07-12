from django.db.models import Avg
from django.core.cache import cache

from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.book.models import Book , Favorite
from apps.book.serializers import BookSerializer,FavoriteSerializer
from apps.review.models import Review
from apps.review.serializer import ReviewSerializer


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.filter(is_active=True)

    def list(self, request):
        cache_key = 'books_list'
        if cache_key in cache:
            print('Data fetched from cache')
            queryset = cache.get(cache_key)
        else:
            print('Data fetched from database')
            queryset = self.filter_queryset(self.get_queryset())
            cache.set(cache_key, list(queryset), timeout=60*60)  # Cache the queryset for an hour

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = f'book_{instance.id}_details'
        cached_data = cache.get(cache_key)

        if cached_data:
            print("Data fetched from cache")
            return Response(cached_data)
        
        print("Data fetched from database")
        serializer = self.get_serializer(instance)
        reviews = Review.objects.filter(book=instance)
        review_serializer = ReviewSerializer(reviews, many=True)
        # Filter reviews for the book to include only active reviews
        reviews = Review.objects.filter(book=instance)
        review_serializer = ReviewSerializer(reviews, many=True)

        # Calculate the average rating for the book
        average_rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        response_data = serializer.data
        response_data['reviews'] = review_serializer.data
        response_data['average_rating'] = average_rating

        cache.set(cache_key, response_data,timeout=60*60)  
        return Response(response_data)

    @action(detail=False, methods=['get'], url_path='top-10-rated')
    def top_rated(self, request):
        cache_key = 'top_10_rated_books'
        cached_data = cache.get(cache_key)

        if cached_data:
            print("Top 10 rated books fetched from cache")
            return Response(cached_data)
        print("Top 10 rated books fetched from database")
        # Get the books with the highest average rating, limiting to top 10
        top_rated_books = Review.objects.values('book').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:10]

        if top_rated_books:
            top_rated_books_list = []
            for book_info in top_rated_books:
                book_id = book_info['book']
                average_rating = book_info['avg_rating']
                book = Book.objects.get(id=book_id)

                serializer = self.get_serializer(book)
                reviews = Review.objects.filter(book=book)
                review_serializer = ReviewSerializer(reviews, many=True)

                book_data = serializer.data
                book_data['reviews'] = review_serializer.data
                book_data['average_rating'] = average_rating

                top_rated_books_list.append(book_data)

            cache.set(cache_key, top_rated_books_list,imeout=60*60)
            return Response(top_rated_books_list)

        return Response({"detail": "No reviews found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user:
            return Response({"msg": "You dont have premission to delete this book."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response({"msg": "book deleted."},status=status.HTTP_200_OK)
    
    def perform_destroy(self, instance):
        instance.is_active=False
        instance.save(update_fields=['is_active'])

    @action(
            detail=True, 
            methods=['post'], 
            permission_classes=[IsAuthenticated]
            )
    def favorite(self, request, pk=None):
        book = self.get_object()
        data = {'book': book.id, 'user': request.user.id}
        serializer = FavoriteSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
            detail=True, 
            methods=['post'], 
            permission_classes=[IsAuthenticated]
            )
    def unfavorite(self, request, pk=None):
        book = self.get_object()
        user = request.user
        favorite = Favorite.objects.filter(book=book, user=user)
        if favorite.exists():
            favorite.delete()
            return Response({'msg': 'Book removed from favorites successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'You have not favorited this book.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(
            detail=False,
            methods=['get'], 
            permission_classes=[IsAuthenticated]
            )
    def my_favorites(self, request):   
        favorites = Favorite.objects.filter(user=request.user)# Fetch all favorites for the authenticated user
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
