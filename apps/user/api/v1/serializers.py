from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    # Create the user with the validated data
    def create(self, validated_data):
        request = self.context.get('request')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # Inactive until email is verified
        user.save()

        # Prepare and send verification email
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
        
        return user

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    def validate(self, attrs):
         # Authenticate the user with the username and password
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = authenticate(username=username, password=password)

        # if authentication fails or user is inactive
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, verify your email first')
        
         # Return user data with token
        return {
            'username': user.username,
            'password': password, 
            'token': Token.objects.get_or_create(user=user)[0].key
        }
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        validate_password(value)  # Validate the new password
        return value

    def validate(self, attrs):       
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Wrong password."})
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password']) # Save the new password
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value) # Check if the email is associated with a user or not
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self, request):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate password reset link
        reset_password_url = reverse('user-reset-password', kwargs={'uid': uid, 'token': token})
        current_site = get_current_site(request).domain
        reset_password_link = f"{request.scheme}://{current_site}{reset_password_url}"
        
         # Prepare and send password reset email
        subject = "Password Reset"
        message = f"Hi {user.username},\n\nYou have requested a password reset." \
                  f"Please click the link below to reset your password:\n\n"\
                  f"{reset_password_link}\n\nIf you did not request this, "\
                  f"please ignore this email.\n\nThank you."

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return user
    
# Serializer for resetting the user's password
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']: # Check if the new passwords match
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    
    # Save the new password
    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()
    default_error_messages = {
        'bad_token': 'Token is expired or invalid'
    }
    # Check if the token is provided or not 
    def validate(self, attrs):
        token = attrs.get('token')
        if not token:
            raise serializers.ValidationError("Token is required.")
        self.token = token
        return attrs

    def save(self, **kwargs):
        try:
            token = Token.objects.get(key=self.token)
            token.delete()         # Delete the token to log out the user
        except Token.DoesNotExist:
            self.fail('bad_token')