from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from apps.review.serializer import ReviewSerializer
from apps.review.models import Review

class ReviewViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Review.objects.all()
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        print("basename:", self.basename)
        print("action:", self.action)
        print("detail:", self.detail)
        print("suffix:", self.suffix)
        print("name:", self.name)
        print("description:", self.description)

        queryset = Review.objects.all()
        review = get_object_or_404(queryset, pk=pk,)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)