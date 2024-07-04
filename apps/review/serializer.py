from rest_framework import serializers
from apps.user.serializer import UserSerializer
from apps.book.serializers import BookSerializer
from apps.book.models import Book
from .models import Review

# Serializer for the Review model
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Review
        fields = ('id', 'book', 'review_text', 'rating','user','book_id')

    #  the create method to set the user field to the current user
    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError('Book not found.')        
        validated_data['user'] = self.context['request'].user
        validated_data['book'] = book
        review = Review.objects.create(**validated_data)
        return review
    
    def validate_rating(self, value):
        if value > 5:
            raise serializers.ValidationError('Rating cannot be more than 5')
        elif value < 1:
            raise serializers.ValidationError('Rating cannot be less than 1')
        return value
