from rest_framework import serializers
from apps.book.models import Book
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(slug_field='title', queryset=Book.objects.all())
    class Meta:
        model = Review
        fields = ('id', 'book', 'user', 'review_text', 'rating', 'created_at')
        read_only_fields = ('user', 'created_at')  #  user and created_at cannot be changed

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        review = Review.objects.create(**validated_data)
        return review

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['book'] = instance.book.title
        representation['user'] = instance.user.username
        return representation