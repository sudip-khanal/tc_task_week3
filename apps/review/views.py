# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from drf_yasg.utils import swagger_auto_schema
# from apps.review.serializer import ReviewSerializer

# @swagger_auto_schema(
#     method='post',
#     operation_summary="Add book review",
#     operation_description="This endpont used to review the book"
# )
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_review(request):
#     serializer = ReviewSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



### viewsets ###
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
        queryset = Review.objects.all()
        review = get_object_or_404(queryset, pk=pk,)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)