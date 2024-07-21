from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers

from apps.user.tasks import send_verification_email,send_reset_email

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # Inactive until email is verified
        user.save()
        send_verification_email.delay(user.id) # Pass the user object to send_verification_email
        return user
       

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
            'email':user.email,
            'token': Token.objects.get_or_create(user=user)[0].key
        }
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):       
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Wrong password."})
        elif attrs['new_password'] != attrs['confirm_new_password']: # Check if the new passwords match
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
    
    def change_password(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password']) # Save the new password
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)  # check if the email is associated with a user or not
        except User.DoesNotExist:
            raise serializers.ValidationError(" User not found with this email address.")
        return value
    
    def send_reset_pass_email(self):
        send_reset_email.delay(self.user.id)

    
# Serializer for resetting the user's password
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']: # Check if the new passwords match
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            uid = force_bytes(urlsafe_base64_decode(self.context['uid']))
            self.user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"msg": "Invalid link."})
        
        if not default_token_generator.check_token(self.user, self.context['token']):
            raise serializers.ValidationError({"msg": "Invalid token."})
        return attrs
    # Save the new password
    def reset_password(self):
        user=self.user
        user.set_password(self.validated_data['new_password'])
        user.save(update_fields=['password'])
        return user