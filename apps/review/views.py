from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.review.serializer import ReviewSerializer

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
