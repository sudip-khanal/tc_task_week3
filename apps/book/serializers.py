from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.book.models import Book,Favorite
from apps.user.serializer import UserSerializer
from apps.review.serializer import ReviewSerializer


class BookSerializer(serializers.ModelSerializer):
    created_by= UserSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'is_active','created_by')
        read_only_fields = ('created_at', 'updated_at',)
        
    # the create method to set the created_by field to the current user
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.created_by != self.context['request'].user:
            raise PermissionDenied("You do not have permission to update this book.")
        return super().update(instance, validated_data)
   
###Favorite book serializer
class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'book']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'You have already added this book to your favorite list.'})



class BookWithAvgRatingSerializer(serializers.Serializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'reviews', 'average_rating')