from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated

from apps.review.serializer import ReviewSerializer
from apps.review.models import Review

class ReviewViewSet(mixins.CreateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes=[IsAuthenticated]
    

