from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator 

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from apps.user.serializer import ( 
    UserSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    LoginSerializer,
    ForgotPasswordSerializer
    )


class RegisterUser(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            response_data = {
                'username': user.username,
                'email': user.email,
                'msg': 'Register successfully. Check your email for verification.'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)               
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'msg': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if default_token_generator.check_token(user, token):
            if user.is_active:
                return Response({'msg': 'Email already verified.'}, status=status.HTTP_400_BAD_REQUEST)
            user.is_active = True
            user.save(update_fields=['is_active'])
            return Response({'msg': 'Email verified successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePassword(GenericAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.change_password()
            return Response({'msg': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.send_reset_email(serializer.validated_data) # Correctly call reset_pass_mail without additional arguments
            return Response({'msg': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ResetPassword(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid():
            serializer.reset_password()
            return Response({'msg': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Logout(APIView):
   permission_classes=[IsAuthenticated]
   def post(self, request):
        logout(request)
        return Response({'msg': 'Logged out successfully.'})