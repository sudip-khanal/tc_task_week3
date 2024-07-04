from django.db import IntegrityError
from rest_framework import serializers
from apps.book.models import Book,Favorite
from apps.user.serializer import UserSerializer

class BookSerializer(serializers.ModelSerializer):
    created_by= UserSerializer(read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'is_active','created_by')
        read_only_fields = ('created_at', 'updated_at',)
        
    # the create method to set the created_by field to the current user
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user 
        book = Book.objects.create(**validated_data)
        return book
    
     # update method to update specific fields of the Book model
    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        if instance.created_by != request_user:
            raise serializers.ValidationError("You don't have permission to update this book.")

        instance.title = validated_data.get('title', instance.title) 
        instance.author = validated_data.get('author', instance.author)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save(update_fields=['title', 'author', 'description', 'is_active'])
        return instance
    
###Favorite book serializer
class FavoriteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    book_id  = serializers.IntegerField(write_only=True) 

    class Meta:
        model = Favorite
        fields = ['id', 'user','book','book_id']
    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        # Lookup the book instance by its title
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError({'msg': 'Book not found.'})
        # Set user to the current request user
        validated_data['user'] = self.context['request'].user
        validated_data['book'] = book
        try:
            favorite = Favorite.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'msg': 'you have already added this book to your favorite book list.'})
        
        return favorite
       