from rest_framework import serializers
from apps.review.models import Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('created_by') 
