from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.book.serializers import BookSerializer
from apps.book.models import Book

# Implementation of ModelViewSet which Abstract curd methods
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_active=True)
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
