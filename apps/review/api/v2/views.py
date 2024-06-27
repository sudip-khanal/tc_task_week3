from rest_framework import viewsets
from apps.review.serializer import ReviewSerializer
from apps.review.models import Review

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer