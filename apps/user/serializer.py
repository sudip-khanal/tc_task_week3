from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    conform_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','conform_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['conform_password']:
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
        verification_url = f"{settings.SITE_URL}{reverse('verify_email', args=[uid, token])}"
        subject = 'Verify your email'
        message = f'Hi {user.username}, please verify your email by clicking the link: {verification_url}'
        send_mail(subject,message,settings.EMAIL_HOST_USER,[user.email])
        return user

class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def verify_email(self, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            return {"error": "Invalid UID"}
        except User.DoesNotExist:
            return {"error": "User does not exist"}

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=['is_active'])
            return {"message": " Email verified successfully"}
        else:
            return {"message": "Invalid token "}


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
    
    def send_reset_email(self, request):
        user = self.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_password_url = reverse('reset_password', kwargs={'uid': uid, 'token': token})
        reset_password_link = f"{settings.SITE_URL}{reset_password_url}"
        subject = "Password Reset"
        message = f"Hi {user.username},Please click the link to reset your password:\n{reset_password_link}"
    
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
    
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