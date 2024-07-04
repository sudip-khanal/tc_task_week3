from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Book, Favorite
from apps.book.serializers import BookSerializer, FavoriteSerializer 

@swagger_auto_schema(
    method='post',
    operation_summary="Add new book",
    operation_description="This endpont add new book"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_create(request):
    serializer = BookSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save() 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_summary="List all the book",
    operation_description="This endpont return all the books"
)
@api_view(['GET'])
def book_list(request):
    books = Book.objects.filter(is_active=True)  # Filter to get only active books
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_summary="Retrive a book",
    operation_description="This endpont retrive a specific book details"
)
@api_view(['GET'])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk, is_active=True)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    operation_summary="Update book",
    operation_description="This endpont update book details"
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.update(book, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='delete',
    operation_summary=" delete the book",
    operation_description="This endpont set the is_active field of book to false"
)
# Endpoint to soft delete a book (set is_active to False)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def book_soft_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.created_by != request.user:
        return Response({'message': 'You do not have permission to delete this book.'}, status=status.HTTP_400_BAD_REQUEST)
    book.soft_delete()  
    return Response({'message': 'Book  deleted successfully'}, status=status.HTTP_200_OK)

## favorite book
@swagger_auto_schema(
    method='post',
    operation_summary="add book to favourite",
    operation_description="This endpont add book to favourite"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite(request):
    serializer = FavoriteSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_summary="retrive favouriet books",
    operation_description="This endpont retrive favouriet books of the user"
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def favourite_book(request):
    favorites = Favorite.objects.filter(user=request.user)
    if favorites.exists():
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "You don't have any favorite books."}, status=status.HTTP_404_NOT_FOUND)




