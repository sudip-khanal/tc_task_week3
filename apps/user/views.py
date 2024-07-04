from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from apps.user.serializer import(
    UserSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer
    )

User = get_user_model()

@swagger_auto_schema(
    method='post',
    operation_summary="register the new user",
    operation_description="This endpont add new user into the system"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Registered successfully. Please verify your email.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(
    method='get',
    operation_summary="verify email",
    operation_description="This endpont verify email address"
)
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    serializer = VerifyEmailSerializer()
    user = serializer.verify_email(uidb64, token)
    if user:
        return Response({'detail': 'Email verified successfully'}, status=status.HTTP_200_OK)
    return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="login ",
    operation_description="This endpont used to authenticate the user and return the token"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.validated_data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_summary="logout the user",
    operation_description="delete the token which is used to authenticate the user"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logout successfully'}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    operation_summary="change user password",
    operation_description="This endpont change the password of user"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.change_password()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="forgot password",
    operation_description="This endpont send the link to reset password to the user email"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.send_reset_email(request)
        return Response({'message': 'Password reset link sended to your email'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@swagger_auto_schema(
    method='post',
    operation_summary="reset password",
    operation_description="This endpont reset password"
)
@api_view(['POST'])
def reset_password(request, uid, token):
    serializer = ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
    if serializer.is_valid():
        serializer.reset_password()
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)