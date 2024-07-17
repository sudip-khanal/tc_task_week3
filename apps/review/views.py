from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated

from apps.review.serializer import ReviewSerializer
from apps.review.models import Review
from apps.review.filters import ReviewFilter

class ReviewViewSet(mixins.CreateModelMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter


