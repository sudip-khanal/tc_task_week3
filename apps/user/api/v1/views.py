from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import (
    RegisterSerializer, VerifyEmailSerializer, ForgotPasswordSerializer,
      ResetPasswordSerializer,LoginSerializer,LogoutSerializer,ChangePasswordSerializer
      )

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class=RegisterSerializer
    
    # Action to register a new user.
    @action(detail=False, methods=['post'], permission_classes=[AllowAny],serializer_class=RegisterSerializer)
    def register(self, request):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registered successfully. Please verify your email.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Action to verify the email using the provided token.
    @action(detail=False, methods=['post'], permission_classes=[AllowAny],serializer_class=VerifyEmailSerializer)
    def verify_email(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        try:
            user = User.objects.get(auth_token=token)
            user.is_active = True
            user.save()
            return Response({'detail': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    #  Action to initiate the password reset process.
    @action(detail=False, methods=['post'], permission_classes=[AllowAny],serializer_class=ForgotPasswordSerializer)
    def forgot_password(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request)
        return Response({'detail': 'Password reset link sent'}, status=status.HTTP_200_OK)
    
    # Action to reset the password using the provided token and UID.
    @action(detail=False, methods=['post'], permission_classes=[AllowAny],serializer_class=ResetPasswordSerializer)
    def reset_password(self, request, uid=None, token=None):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': 'Invalid user ID'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            serializer.save(user=user)
            return Response({'detail': 'Password reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Action to authenticate and login a user.
    @action(detail=False, methods=['post'], permission_classes=[AllowAny],serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    # Action to logout the authenticated user by deleting their token.
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated],serializer_class=LogoutSerializer)
    def logout(self,request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Action to change the authenticated user's password.
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated],serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
