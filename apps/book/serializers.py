from django.contrib.auth.models import User
from rest_framework import serializers
from apps.book.models import Book,Favorite

class BookSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'created_by', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at', 'created_by')
        
    #Overriding the create method to set the created_by field to the current user
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        book = Book.objects.create(**validated_data)
        return book
    
     # Overriding the update method to update specific fields of the Book model
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.description = validated_data.get('description', instance.description)
        instance.is_active = validated_data.get('is_active', instance.is_active)

        instance.save(update_fields=['title', 'author', 'description', 'is_active', 'password'])
        return instance
    
###Favorite book serializer
class FavoriteSerializer(serializers.ModelSerializer):
    #user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    book = serializers.SlugRelatedField(slug_field='title', queryset=Book.objects.all())

    class Meta:
        model = Favorite
        fields = ('id', 'user', 'book')
        read_only_fields = ('user',)  

#validation to ensure a user cannot favorite the same book more than once
    def validate(self, attrs):
        user = self.context['request'].user
        book = attrs['book']
        if Favorite.objects.filter(user=user, book=book).exists():
            raise serializers.ValidationError("You have already favorited this book.")
        return attrs

    """  Overriding the create method to set the user field to the current user """ 
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        favorite = Favorite.objects.create(**validated_data)
        return favorite
    
    """  representation to include user and book titles instead of ids""" 
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['book'] = instance.book.title
        return representation


