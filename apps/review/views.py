from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from drf_yasg.utils import swagger_auto_schema
from apps.review.serializer import ReviewSerializer
from apps.review.models import Review

@swagger_auto_schema(
    method='post',
    operation_summary="Add book review",
    operation_description="This endpont used to review the book"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    serializer = ReviewSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_review(request):
    reviws =Review.objects.all()
    serializer = ReviewSerializer(reviws,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



