from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from apps.book.models import Book , Favorite
from apps.book.serializers import BookSerializer,FavoriteSerializer
from apps.review.models import Review
from apps.review.serializer import ReviewSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset=Book.objects.filter(is_active=True)
    serializer_class=BookSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        reviews = Review.objects.filter(book=instance) # Get the reviews for the book
        review_serializer = ReviewSerializer(reviews, many=True)
        response_data = serializer.data  # Add the serialized reviews to the response data
        response_data['reviews'] = review_serializer.data
        return Response(response_data)
    
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
        favorites = Favorite.objects.filter(user=request.user)        # Fetch all favorites for the authenticated user
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
