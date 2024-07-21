from rest_framework import serializers

from apps.book.models import Book
from apps.review.models import Review
from apps.user.serializer import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Review
        fields = ('id', 'review_text', 'rating', 'user', 'book')

    def validate_rating(self, value):
        if value > 5 or value < 1:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        review = Review.objects.create(**validated_data)
        return review