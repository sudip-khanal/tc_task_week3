from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from apps.user.serializer import *

# Create your views here.
User = get_user_model()

@swagger_auto_schema(
    method='post',
    operation_summary="register the new user",
    operation_description="This endpont add new user into the system"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request).domain
        verification_link = f"{request.scheme}://{current_site}/user/verify-email/{uid}/{token}/"
        message = f'Hi {user.username}, Use the link below to verify your email \n{verification_link}'
        subject = 'Verify your email address'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return Response({'message': 'User registered successfully. Please verify your email.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_summary="verify email",
    operation_description="This endpont verify email address"
)
@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="login ",
    operation_description="This endpont used to authenticate the user and return the token"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                return Response({'detail': 'Account disabled, verify your email first'}, status=status.HTTP_403_FORBIDDEN)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="logout the user",
    operation_description="delete the token which is used to authenticate the user"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    serializer = LogoutSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer.save()
        return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



